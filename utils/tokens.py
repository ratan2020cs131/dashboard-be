import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_session_token(email):
    return jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(minutes=5)}, settings.SECRET_KEY, algorithm='HS256')

def generate_access_token(email):
    return jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(days=30)}, settings.SECRET_KEY, algorithm='HS256')

def decode_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])