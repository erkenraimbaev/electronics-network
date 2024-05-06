from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.permissions import IsAdminAndIsActive, IsSuperUser
from users.serializers import UserSerializer, MyTokenObtainPairSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminAndIsActive]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminAndIsActive]


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_stuff=True, is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        data = request.data
        user_id = data.get('id')
        user_update = get_object_or_404(User, pk=user_id)
        if user_update == self.request.user:
            user_update.set_password(user_update.password)
            user_update.save()
        else:
            message = f'Вы не можете редактировать данный профиль!'
            return Response({"message": message})


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        data = request.data
        user_id = data.get('id')
        user_delete = get_object_or_404(User, pk=user_id)
        if user_delete == self.request.user or self.request.user.is_superuser:
            user_delete.save()
        else:
            message = f'Вы не можете удалить данный профиль!'
            return Response({"message": message})


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
        if user_.role == 'admin':
            if user_.is_active:
                user_.is_active = False
                message = f'Админ {user_.last_name} не имеет больше доступ к API!'
                user_.save()
            else:
                user_.is_active = True
                message = f'Админ {user_.last_name} является активным сотрудником!'
                user_.save()
        else:
            message = f'Этот пользователь не является админом!'

        return Response({"message": message})
