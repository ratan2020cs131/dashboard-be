from django.urls import path
from . import views

urlpatterns = [
    path('get-unapproved', views.get_unapproved_institutes),
]
