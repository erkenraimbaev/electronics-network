import django_filters
from main.models import NetworkLink


class MyNetworkLinkFilter(django_filters.rest_framework.FilterSet):
    """
    Фильтрация объектов по названию страны через контроллер вывода всех объектов
    """
    title = django_filters.CharFilter(field_name="country", lookup_expr="icontains", )

    class Meta:
        model = NetworkLink
        fields = ("country",)
