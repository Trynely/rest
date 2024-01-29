# Generated by Django 4.2.5 on 2024-01-24 16:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0002_alter_purchases_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchases',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='purchases',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
    ]