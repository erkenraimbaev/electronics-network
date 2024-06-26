# Generated by Django 5.0.4 on 2024-05-05 11:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='networklink',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AddField(
            model_name='product',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AlterField(
            model_name='networklink',
            name='network_level',
            field=models.CharField(choices=[(1, 'Продает другому поставщику'), (0, 'Производитель'), (2, 'Продает потребителю')], verbose_name='уровень структуры'),
        ),
        migrations.AlterField(
            model_name='networklink',
            name='product',
            field=models.ManyToManyField(related_name='products_networklink', to='main.product', verbose_name='продукт'),
        ),
    ]
