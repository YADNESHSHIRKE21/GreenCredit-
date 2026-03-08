from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer, UserProfileSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)