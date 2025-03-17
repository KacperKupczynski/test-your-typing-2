from django.shortcuts import render
from rest_framework import Response
from .models import User
from .serializers import UserSerializer 

# Create your views here.

class RegisterView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return Response( {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=201)