from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_institute, name='create_institute'),
    path('get', views.get_institute, name='get_institute'),
]
