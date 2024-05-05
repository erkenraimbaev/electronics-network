from django.contrib import admin

from main.models import Product, NetworkLink


@admin.register(Product)
class AdAdmin(admin.ModelAdmin):
    """
    Ссылка на товары в админ панели
    """
    list_display = ('title', 'launch_date',)
    list_filter = ('title', 'launch_date',)
    search_fields = ('title',)


@admin.register(NetworkLink)
class ReviewAdmin(admin.ModelAdmin):
    """
    Вывод в админке звена сети электроники с сслыкой на поставщика
    """
    list_display = ('title', 'network_level', 'supplier', 'country', 'city', 'debt_to_supplier', 'created_at')
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
