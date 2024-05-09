from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.permissions import IsAdminAndIsActive, IsSuperUser, IsOwnerProfile
from users.serializers import UserSerializer, MyTokenObtainPairSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminAndIsActive]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfile, IsAdminAndIsActive]


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_stuff=True, is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfile]

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerProfile]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SetAdminIsNotActivePostAPIView(APIView):
    """
    Контроллер для суперпользователя, поможет через API сделать сотрудников активными или нет
    """
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = User.objects.all()

    def post(self, request, **kwargs):
        user_id = self.kwargs.get('pk')
        user_ = get_object_or_404(User, pk=user_id)
        if user_.is_active:
            user_.is_active = False
            message = f'Админ {user_.last_name} не имеет больше доступ к API!'
            user_.save()
        else:
            user_.is_active = True
            message = f'Админ {user_.last_name} является активным сотрудником!'
            user_.save()

        return Response({"message": message})
