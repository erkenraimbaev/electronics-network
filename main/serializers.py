from rest_framework import serializers

from main.models import NetworkLink, Product
from main.validators import NoSupplierNoDebtValidator, StructureIsRightValidator


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class NetworkLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkLink
        fields = '__all__'


class NetworkLinkCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NetworkLink
        fields = '__all__'
        validators = [
            StructureIsRightValidator(fields),
            NoSupplierNoDebtValidator(supplier='supplier', debt_to_supplier='debt_to_supplier')

        ]


class NetworkLinkUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NetworkLink
        fields = '__all__'
        validators = [
            StructureIsRightValidator(fields),
            NoSupplierNoDebtValidator(supplier='supplier', debt_to_supplier='debt_to_supplier')

        ]
        # Запрет на обновление дебиторской задолженности через контроллер
        read_only_fields = ["debt_to_supplier"]


class ProductsNetworkLinkSerializer(serializers.ModelSerializer):
    network_links = NetworkLinkSerializer(source='products_networklink', read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'
