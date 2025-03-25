from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Text

class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

#returning all texts
class TextListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        texts = Text.objects.all()
        return Response({'texts': [text.content for text in texts]}, status=status.HTTP_200_OK)
    
#adding a text
class AddTextView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        content = request.data.get('content')
        text = Text(content=content)
        text.save()
        return Response({'content': text.content}, status=status.HTTP_201_CREATED)
    
#deleting a text
class DeleteTextView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        content = request.data.get('content')
        text = Text.objects.get(content=content)
        text.delete()
        return Response({'content': text.content}, status=status.HTTP_200_OK)

#updating a text
class UpdateTextView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        old_content = request.data.get('old_content')
        new_content = request.data.get('new_content')
        text = Text.objects.get(content=old_content)
        text.content = new_content
        text.save()
        return Response({'content': text.content}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    return Response({'username': user.username}, status=status.HTTP_200_OK)