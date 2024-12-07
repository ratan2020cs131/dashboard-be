from django.urls import path, include
from .views import SayHello

urlpatterns = [
    path('user/', include('users.urls')),
    path('superadmin/', include('superadmin.urls')),
    path('institute/', include('institute.urls')),
    path('', SayHello.as_view(), name='say_hello'),
]
