# Generated by Django 4.2.5 on 2023-12-09 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0006_things_img2_things_img3'),
    ]

    operations = [
        migrations.RenameField(
            model_name='things',
            old_name='img',
            new_name='one_img',
        ),
        migrations.RenameField(
            model_name='things',
            old_name='img2',
            new_name='two_img',
        ),
        migrations.RemoveField(
            model_name='things',
            name='img3',
        ),
    ]
