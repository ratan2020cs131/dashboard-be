from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from utils.tokens import decode_token
import jwt
from .services import get_user_by_email

def authentication(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        access_token = request.headers.get('Authorization')  # Get token from headers
        if not access_token:
            return Response({'message': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            decoded_token = decode_token(access_token)
            email = decoded_token['email']
        except jwt.PyJWTError as e:
            return Response({'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
        user = get_user_by_email(email)
        print(user)
        if not user:
            return Response({'message': 'User not found'}, status=404)
        request.user=user
        
        return view_func(request, *args, **kwargs)
    return wrapper
