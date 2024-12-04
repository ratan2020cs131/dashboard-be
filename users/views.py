from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import SigninSerializer, VerifyUserSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from .services import get_user_by_email
from utils.generate_otp import generate_otp
from utils.tokens import generate_session_token,decode_token, generate_access_token
from utils.send_otp import send_otp_via_email
import jwt
from .decorators import authentication

@csrf_exempt
@api_view(['POST'])
def create_user(request):
    serializer = SigninSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        user=get_user_by_email(email)
        otp = generate_otp()
        if user:
            user.otp = otp
            user.save()
        else:
            otp = otp
            user = User.objects.create(email=email, otp=otp)

        session_token = generate_session_token(email)
        send_otp_via_email(email, otp)
        return Response(
                {
                "session_token":session_token,
                "message":f"OTP has been sent to {email}"
                }, 
                status=status.HTTP_201_CREATED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def verify_user(request):
    serializer = VerifyUserSerializer(data=request.data)
    if serializer.is_valid():
        session_token = serializer.validated_data.get('session_token')
        otp = serializer.validated_data.get('otp')

        try:
            decoded_token = decode_token(session_token)
            email = decoded_token['email']
        except jwt.PyJWTError as e:
            return Response({'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
        user = get_user_by_email(email)
        
        if user.otp != otp:
            return Response({'message': 'Invalid otp'}, status=status.HTTP_400_BAD_REQUEST)
        
        access_token = generate_access_token(email)
        user.otp=None
        user.save()

        return Response(
                {
                "access_token":access_token,
                "message": "User verified successfully."
                }, 
                status=status.HTTP_200_OK
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
@authentication
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response({'message': 'User found', 'user': serializer.data})