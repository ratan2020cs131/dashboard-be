import jwt
import random
import string
from datetime import datetime, timedelta
from django.conf import settings
from smtplib import SMTP
from decouple import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_session_token(email):
    return jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(minutes=5)}, settings.SECRET_KEY, algorithm='HS256')

def generate_access_token(email):
    return jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(hours=1)}, settings.SECRET_KEY, algorithm='HS256')

def send_otp_via_email(email, otp):
    try:
        # Email server configuration
        smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
        smtp_port = 587
        sender_email = "ratandeep.blr.12@gmail.com"  # Replace with your email
        sender_password = config('GMAIL_APP_PASSWORD')  # Replace with your email password or app password
        
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Authentication OTP from Senarius"
        body = f"Your OTP code to login into Senarius is: {otp}"
        msg.attach(MIMEText(body, 'plain'))
        
        # Send the email
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, email, msg.as_string())
        smtp.quit()
        print(f"OTP sent to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))
