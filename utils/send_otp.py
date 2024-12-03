import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

def send_otp_via_email(email, otp):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "ratandeep.blr.12@gmail.com"
        sender_password = config('GMAIL_APP_PASSWORD')
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Authentication OTP from Senarius"
        body = f"Your OTP code to login into Senarius is: {otp}"
        msg.attach(MIMEText(body, 'plain'))
        
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, email, msg.as_string())
        smtp.quit()
        print(f"OTP sent to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")
