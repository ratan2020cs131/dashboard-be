from django.urls import path, include
from .views import SayHello

urlpatterns = [
    path('auth/', include('authapp.urls')),
    path('', SayHello.as_view(), name='say_hello'),
]
