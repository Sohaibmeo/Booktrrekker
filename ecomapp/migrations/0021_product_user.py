# Generated by Django 4.0.1 on 2022-06-27 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0020_delete_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.TextField(default='Admin', max_length=20),
        ),
    ]
