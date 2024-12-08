from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import Institute
from .serializers import InstituteSerializer
from users.decorators import authentication, authorize_roles
from constants.roles import Roles

@csrf_exempt
@api_view(['POST'])
@authentication
@authorize_roles([Roles.ADMIN, Roles.SUPERADMIN])
def create_institute(request):
    request.data['user'] = request.user.id
    serializer = InstituteSerializer(data=request.data)
    if serializer.is_valid():
        institute_code = serializer.validated_data.get('institute_code')
        
        # Check if institute code already exists
        if Institute.objects.filter(institute_code=institute_code).exists():
            return Response(
                {'message': 'Institute code already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(
            {
                'message': 'Institute created successfully',
                'institute': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
@authentication
@authorize_roles([Roles.ADMIN, Roles.SUPERADMIN])
def get_institute(request):
    try:
        institute = Institute.objects.select_related('user').get(user=request.user.id)
        serializer = InstituteSerializer(institute, context={'request': request})
        return Response(
            {
                'message': 'Institute retrieved successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Institute.DoesNotExist:
        return Response(
            {'message': 'Institute not found'},
            status=status.HTTP_404_NOT_FOUND
        )
