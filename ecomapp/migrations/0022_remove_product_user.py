# Generated by Django 4.0.1 on 2022-06-27 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0021_product_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
    ]
