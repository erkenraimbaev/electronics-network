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

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        network_level = dict(value).get('network_level')
        supplier = dict(value).get('supplier')
        if supplier:
            supplier_level = int(supplier.network_level)
            if network_level == 0 and supplier_level == 1 or supplier_level == 2:
                raise serializers.ValidationError(
                    "У производителя не может быть поставщика уровня 1(посредника) и уровня 2(продавца потребителю)"
                )
            if network_level == 1 and supplier_level == 2:
                raise serializers.ValidationError(
                    "У звена уровня 1 (посредника) не может быть поставщика уровня 2(продавца конечному потребителю)"
                )
