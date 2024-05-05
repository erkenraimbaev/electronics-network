from django.db import models

NULLABLE = {"blank": True, "null": True}


class Product(models.Model):
    """
    Модель товара
    """
    title = models.CharField(max_length=100, verbose_name='название')
    product_model = models.CharField(max_length=100, verbose_name='продуктовая модель', **NULLABLE)
    launch_date = models.DateField(verbose_name='дата выхода товара на рынок')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


class NetworkLink(models.Model):
    """
    Модель для звена в сети по продаже электроники
    Иерархическая структура сети:
    Уровень 0: Производитель(завод)
        Поставщиком может быть: Завод
    Уровень 1: Продает другому поставщику
        Поставщиком может быть: Завод, Розничная сеть
    Уровень 2: Продает потребителю
        Поставщиком может быть: Розничная сеть, завод, ИП
    """

    LEVELS = {
        (0, 'Производитель'),
        (1, 'Продает другому поставщику'),
        (2, 'Продает потребителю'),
    }

    network_level = models.CharField(choices=LEVELS, verbose_name='уровень структуры')
    title = models.CharField(max_length=100, unique=True, verbose_name='название.')
    email = models.EmailField(unique=True, verbose_name='почта')
    country = models.CharField(max_length=100, verbose_name='страна')
    city = models.CharField(max_length=100, verbose_name='город')
    street = models.CharField(max_length=100, verbose_name='улица')
    house_number = models.PositiveSmallIntegerField(verbose_name='дом')
    product = models.ManyToManyField(Product, verbose_name='продукт')
    supplier = models.ForeignKey('self', on_delete=models.PROTECT, verbose_name='поставщик', **NULLABLE)
    debt_to_supplier = models.DecimalField(decimal_places=2,
                                           max_digits=15,
                                           verbose_name='Задолженность перед поставщиком с точностью до копеек',
                                           **NULLABLE)
    created_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Время создания(заполняется автоматически при создании)')

    def __str__(self):
        return f'Название: {self.title}, Уровень: {self.network_level}, Контакты: {self.email}'

    class Meta:
        verbose_name = "звено сети по продаже электроники"
        verbose_name_plural = "звенья сети по продаже электроники"
