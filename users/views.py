from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def register(request):
    """User registration"""
    data = request.data
    if User.objects.filter(username=data['username']).exists():
        return Response({'error': 'User already exists'}, status=400)

    user = User.objects.create_user(username=data['username'], password=data['password'], email=data['email'])
    return Response({'message': 'User registered successfully'}, status=201)


@api_view(['POST'])
def login(request):
    """User login and JWT token generation"""
    data = request.data
    user = authenticate(username=data['username'], password=data['password'])

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    return Response({'error': 'Invalid credentials'}, status=400)


@api_view(['POST'])
def logout(request):
    """Logout by blacklisting the refresh token"""
    try:
        token = request.data.get('refresh_token')
        if token:
            RefreshToken(token).blacklist()
        return Response({'message': 'Logged out successfully'}, status=200)
    except Exception:
        return Response({'error': 'Invalid token'}, status=400)

class VerifyTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Token is valid"}, status=200)