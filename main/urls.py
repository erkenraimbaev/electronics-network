from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.apps import MainConfig
from main.views import ProductViewSet, NetworkLinkListView, NetworkLinkCreateView, MyNetworkLinkListView, \
    NetworkLinkDetailView, NetworkLinkUpdateView, NetworkLinkDeleteView, ProductsNetworkLinkDetailView

app_name = MainConfig.name

product_router = DefaultRouter()
product_router.register(r"product", ProductViewSet, basename="product")

urlpatterns = [
    path('network_links/', NetworkLinkListView.as_view(), name='network-links-list'),
    path('network_links/create/', NetworkLinkCreateView.as_view(), name='network-link-create'),
    path('network_links/me/', MyNetworkLinkListView.as_view(), name='my-network-link-list'),
    path('network_links/<int:pk>/', NetworkLinkDetailView.as_view(), name='network-link-detail'),
    path('network_links/update/<int:pk>/', NetworkLinkUpdateView.as_view(), name='network-link-update'),
    path('network_links/delete/<int:pk>/', NetworkLinkDeleteView.as_view(), name='network-link-delete'),
    path('product/<int:pk>/network_links/', ProductsNetworkLinkDetailView.as_view(), name='product-detail'
                                                                                          '-network-links'),
    path('products/', include(product_router.urls)),
]
