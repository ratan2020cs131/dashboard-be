from django.urls import path
from .views import EmailCheckAPI, VerifyOTPAPI

urlpatterns = [
    path('check-email/', EmailCheckAPI.as_view(), name='check_email'),
    path('verify-otp/', VerifyOTPAPI.as_view(), name='verify_otp'),
]
