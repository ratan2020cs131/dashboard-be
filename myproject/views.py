from rest_framework.views import APIView
from rest_framework.response import Response

class SayHello(APIView):
    def get(self, request):
        return Response({"message":"Senarius backend is running"})