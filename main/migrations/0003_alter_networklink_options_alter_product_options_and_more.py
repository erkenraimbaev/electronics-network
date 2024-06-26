# Generated by Django 5.0.4 on 2024-05-06 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_networklink_author_product_author_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='networklink',
            options={'ordering': ['network_level'], 'verbose_name': 'звено сети по продаже электроники', 'verbose_name_plural': 'звенья сети по продаже электроники'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-launch_date'], 'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
        migrations.AlterField(
            model_name='networklink',
            name='network_level',
            field=models.CharField(choices=[(2, 'Продает потребителю'), (0, 'Производитель'), (1, 'Продает другому поставщику')], verbose_name='уровень структуры'),
        ),
    ]
