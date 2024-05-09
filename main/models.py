from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Product(models.Model):
    """
    Модель товара
    """
    title = models.CharField(max_length=100, verbose_name='название')
    product_model = models.CharField(max_length=100, verbose_name='продуктовая модель', **NULLABLE)
    launch_date = models.DateField(verbose_name='дата выхода товара на рынок')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ['-launch_date']


class NetworkLink(models.Model):
    """
    Модель для звена в сети по продаже электроники
    Иерархическая структура сети:
    Теоретически у каждого из уровней может быть поставщик - ограничение в уровне иерархии
    (он может быть равен или ниже, математически выше)
    Уровень 0: Поставщик - Производитель
        Поставщиком здесь может быть: производитель уровня 0(Покупает запчати у другого завода доделывает и продает
        посреднику или продавцу для потребителей)
    Уровень 1: Поставщик - Розничная сеть, продает другому поставщику или потребителю
        (Посредник или продавец потребителю)
        Поставщиком может быть: уровни 0 или 1
    Уровень 2: Поставщик - ИП
        Поставщиком может быть: уровни 0, 1, 2
    """

    LEVELS = {
        (0, 'Поставщик - производитель'),
        (1, 'Поставщик - розничная сеть'),
        (2, 'Поставщик - индивидуальный предприниматель'),
    }

    network_level = models.CharField(choices=LEVELS, verbose_name='уровень структуры')
    title = models.CharField(max_length=100, unique=True, verbose_name='название.')
    email = models.EmailField(unique=True, verbose_name='почта')
    country = models.CharField(max_length=100, verbose_name='страна')
    city = models.CharField(max_length=100, verbose_name='город')
    street = models.CharField(max_length=100, verbose_name='улица')
    house_number = models.PositiveSmallIntegerField(verbose_name='дом')
    product = models.ManyToManyField(Product, verbose_name='продукт', related_name='products_networklink', **NULLABLE)
    supplier = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='поставщик', **NULLABLE)
    debt_to_supplier = models.DecimalField(decimal_places=2,
                                           max_digits=15,
                                           verbose_name='Задолженность перед поставщиком с точностью до копеек',
                                           **NULLABLE)
    created_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Время создания(заполняется автоматически при создании)')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)

    def __str__(self):
        return f'Название: {self.title}, Уровень: {self.network_level}, Контакты: {self.email}'

    class Meta:
        verbose_name = "звено сети по продаже электроники"
        verbose_name_plural = "звенья сети по продаже электроники"
        ordering = ['network_level']
