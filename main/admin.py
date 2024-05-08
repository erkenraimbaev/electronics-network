from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from main.models import Product, NetworkLink


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Ссылка на товары в админ панели
    """
    list_display = ('title', 'launch_date',)
    list_filter = ('title', 'launch_date',)
    search_fields = ('title',)


@admin.register(NetworkLink)
class NetworkLinkAdmin(admin.ModelAdmin):
    """
    Вывод в админке звена сети электроники с сслыкой на поставщика
    """
    list_display = ('title', 'network_level', 'display_supplier', 'country', 'city', 'debt_to_supplier', 'created_at')

    # Кликабельная ссылка на поставщика в админке
    def display_supplier(self, obj):
        link = reverse("admin:main_networklink_change", args=[obj.id])
        return format_html('<a href="{}">{}</a>', link, obj.supplier)

    display_supplier.short_description = "Поставщик"

    # фильтр по названию города
    list_filter = ('city',)
    search_fields = ('title',)
    actions = ["clear_debt_to_supplier"]

    @admin.action(description="Очистить дебиторскую задолженность")
    def clear_debt_to_supplier(self, request, queryset):
        """
        админ экшион, очищающет задолженность перед поставщиком у выбранных объектов.
        """
        queryset.update(debt_to_supplier=0)
