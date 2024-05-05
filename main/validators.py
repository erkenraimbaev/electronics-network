from rest_framework import serializers


class NoSupplierNoDebtValidator:
    """
    Если у звена нет поставщика - не может быть дебиторской задолженности
    """
    def __init__(self, supplier, debt_to_supplier):
        self.supplier = supplier
        self.debt_to_supplier = debt_to_supplier

    def __call__(self, value):
        supplier = value.get(self.supplier)
        debt_to_supplier = value.get(self.debt_to_supplier)

        if not supplier and debt_to_supplier:
            raise serializers.ValidationError("Без поставщика не может быть дебиторской задолженности!")


class StructureIsRightValidator:
    """
    Проверка на соответствие иерархии
    """

    def __init__(self, supplier, network_level):
        self.supplier = supplier
        self.network_level = network_level

    def __call__(self, value):
        network_level = value.get(self.network_level)
        supplier = value.get(self.supplier)
        if network_level == 0 and supplier.network_level == 2 or supplier.network_level == 1:
            raise serializers.ValidationError(
                "У производителя не может быть поставщика уровня 1(посредника) и уровня 2(продавца потребителю)"
            )
        elif network_level == 1 and supplier.network_level == 2:
            raise serializers.ValidationError(
                "У звена уровня 1 (посредника) не может быть поставщика уровня 2(продавца конечному потребителю)"
            )
