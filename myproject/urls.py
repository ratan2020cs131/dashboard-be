from django.urls import path, include
from .views import SayHello

urlpatterns = [
    path('superadmin/', include('superadmin.urls')),
    path('user/', include('users.urls')),
    path('', SayHello.as_view(), name='say_hello'),
]
