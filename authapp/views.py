import jwt
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .mongo_client import db
from .utils import generate_session_token, generate_access_token, generate_otp, send_otp_via_email

class EmailCheckAPI(APIView):
    def post(self, request):
        print({"email": request.data.get('email')})
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        users_collection = db['users']
        user = users_collection.find_one({'email': email})

        otp = generate_otp()
        if not user:
            users_collection.insert_one({'email': email, 'otp': otp})
        else:
            users_collection.update_one({'email': email}, {'$set': {'otp': otp}})

        session_token = generate_session_token(email)
        send_otp_via_email(email, otp)

        return Response({'session_token': session_token, 'message': 'OTP sent to email'})

class VerifyOTPAPI(APIView):
    def post(self, request):
        session_token = request.data.get('session_token')
        otp = request.data.get('otp')

        if not session_token or not otp:
            return Response({'error': 'Session token and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = jwt.decode(session_token, config('SECRET_KEY'), algorithms=['HS256'])
            email = decoded_token['email']
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Session token expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid session token'}, status=status.HTTP_400_BAD_REQUEST)

        users_collection = db['users']
        user = users_collection.find_one({'email': email, 'otp': otp})

        if not user:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = generate_access_token(email)
        users_collection.update_one({'email': email}, {'$unset': {'otp': 1}})

        return Response({'access_token': access_token, 'message': 'OTP verified'})

