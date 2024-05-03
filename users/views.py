from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.permissions import IsOwner, IsAdmin
from users.serializers import UserSerializer, MyTokenObtainPairSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsAdmin]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsOwner]


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsOwner]

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & IsOwner | IsAdmin]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
