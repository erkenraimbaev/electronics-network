from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from main.filters import MyNetworkLinkFilter
from main.models import Product, NetworkLink
from main.paginators import NetworkLinkPaginator
from main.serializers import ProductSerializer, NetworkLinkSerializer, NetworkLinkCreateSerializer, \
    NetworkLinkUpdateSerializer, ProductsNetworkLinkSerializer
from users.permissions import IsAdminAndIsActive, IsOwner


class ProductViewSet(viewsets.ModelViewSet):
    """
    Контроллер для механизма CRUD товаров
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):

        if self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsAdminAndIsActive]
        elif self.action == "create":
            permission_classes = [IsAuthenticated, IsAdminAndIsActive]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsAdminAndIsActive, IsOwner]
        elif self.action in ["destroy"]:
            permission_classes = [IsAuthenticated, IsAdminAndIsActive, IsOwner]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        product = serializer.save()
        product.author = self.request.user
        product.save()

    def perform_update(self, serializer):
        update_product = serializer.save()
        update_product.author = self.request.user
        update_product.save()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class NetworkLinkListView(generics.ListAPIView):
    """
    Вывести список всех объектов сети по продаже электроники
    Есть пагинация по выводу 10 объектов на странице и фильтр по названию страны
    """
    queryset = NetworkLink.objects.all()
    serializer_class = NetworkLinkSerializer
    pagination_class = NetworkLinkPaginator
    permission_classes = [IsAuthenticated, IsAdminAndIsActive]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MyNetworkLinkFilter


class NetworkLinkCreateView(generics.CreateAPIView):
    """
    Создать объект сети по продаже электроники
    Есть валидация полей: уровень, поставщик и задолженность
    """
    serializer_class = NetworkLinkCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminAndIsActive]

    def perform_create(self, serializer):
        network_link = serializer.save()
        network_link.author = self.request.user
        network_link.save()


class MyNetworkLinkListView(generics.ListAPIView):
    """
    Вывести список своих объектов сети по продаже электроники - пользователь это автор
    """
    serializer_class = NetworkLinkSerializer
    permission_classes = [IsAuthenticated, IsAdminAndIsActive]
    pagination_class = NetworkLinkPaginator

    def get_queryset(self):
        return NetworkLink.objects.filter(author=self.request.user)


class NetworkLinkDetailView(generics.RetrieveAPIView):
    """
    Просмотреть объект сети по продаже электроники
    """
    queryset = NetworkLink.objects.all()
    serializer_class = NetworkLinkSerializer
    permission_classes = [IsAuthenticated, IsAdminAndIsActive]


class NetworkLinkUpdateView(generics.UpdateAPIView):
    """
    Обновить объект сети по продаже электроники
    Есть валидация полей: уровень, поставщик и задолженность
    Нельзя обновлять поле дебиторской задолженности
    """
    queryset = NetworkLink.objects.all()
    serializer_class = NetworkLinkUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminAndIsActive, IsOwner]

    def perform_update(self, serializer):
        update_network_link = serializer.save()
        update_network_link.author = self.request.user
        update_network_link.save()


class NetworkLinkDeleteView(generics.DestroyAPIView):
    """
    Удалить объект сети по продаже электроники
    """
    queryset = NetworkLink.objects.all()
    serializer_class = NetworkLinkSerializer
    permission_classes = [IsAuthenticated, IsAdminAndIsActive, IsOwner]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class ProductsNetworkLinkDetailView(generics.RetrieveAPIView):
    """
    Подробный вывод объектов сети по конкретному продукту
    Видно какие именно поставщики импользуют этот продукт
    """
    queryset = Product.objects.all()
    serializer_class = ProductsNetworkLinkSerializer
    permission_classes = [IsAuthenticated, IsAdminAndIsActive]
