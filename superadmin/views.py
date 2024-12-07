from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.decorators import authentication, authorize_roles
from constants.roles import Roles

@csrf_exempt
@api_view(['GET'])
@authentication
@authorize_roles([Roles.SUPERADMIN])
def get_unapproved_institutes(request):
    return Response({'message':'Hello from super admin'})