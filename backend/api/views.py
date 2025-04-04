from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Text, WpmResult

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
    
#returning a random text
class RandomTextView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        text = Text.objects.order_by('?').first()
        if text is None:
            return Response({'error': 'No texts available'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'content': text.content}, status=status.HTTP_200_OK)    
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

    def delete(self, request):
        content = request.data.get('content')
        try:
            text = Text.objects.get(content=content)
            text.delete()
            return Response({'message': 'Text deleted successfully'}, status=status.HTTP_200_OK)
        except Text.DoesNotExist:
            return Response({'error': 'Text not found'}, status=status.HTTP_404_NOT_FOUND)
        
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
    
class SaveResultView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        text_content = request.data.get('text')
        wpm = request.data.get('wpm')
        user = request.user.username

        try:
            text = Text.objects.get(content=text_content)
            result = WpmResult(text=text, wpm=wpm, user=user)
            result.save()
            return Response({'message': 'Result saved successfully'}, status=status.HTTP_201_CREATED)
        except Text.DoesNotExist:
            return Response({'error': 'Text not found'}, status=status.HTTP_404_NOT_FOUND)
class GetResultView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user.username
        results = WpmResult.objects.filter(user=user).order_by('-created_at')
        serialized_results = [{'text': result.text.content, 'wpm': result.wpm} for result in results]
        return Response({'results': serialized_results}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    return Response({'username': user.username}, status=status.HTTP_200_OK)