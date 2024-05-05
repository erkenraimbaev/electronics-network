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


class NetworkLinkCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkLink
        fields = (
            'network_level', 'title', 'email', 'country', 'city', 'street', 'house_number', 'supplier',
            'debt_to_supplier',)
        validators = [
            StructureIsRightValidator(network_level='network_level', supplier='supplier'),
            NoSupplierNoDebtValidator(supplier='supplier', debt_to_supplier='debt_to_supplier')

        ]
