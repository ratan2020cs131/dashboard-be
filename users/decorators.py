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
        if not user:
            return Response({'message': 'User not found'}, status=404)
        request.user=user
        
        return view_func(request, *args, **kwargs)
    return wrapper

def authorize_roles(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Ensure `request.user` is set by the `authentication` decorator
            user = getattr(request, 'user', None)
            if not user or not hasattr(user, 'role'):
                return Response({'message': 'User role not found or user not authenticated'}, status=status.HTTP_403_FORBIDDEN)
            
            # Check if user's role is in the allowed roles
            allowed_roles_values = [role.value for role in allowed_roles]
            if user.role not in allowed_roles_values:
                return Response({'message': 'Forbidden: You do not have access to this resource'}, status=status.HTTP_403_FORBIDDEN)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator