# Generated by Django 4.2.5 on 2024-01-23 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0008_purchases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchases',
            name='selected_size',
            field=models.IntegerField(verbose_name='Выбранный размер'),
        ),
    ]
