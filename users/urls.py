from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.create_user),
    path('verify', views.verify_user),
]
