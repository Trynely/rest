# Generated by Django 5.0.1 on 2024-01-31 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0004_alter_purchases_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchases',
            options={'verbose_name': 'Покупка', 'verbose_name_plural': 'Покупки'},
        ),
    ]