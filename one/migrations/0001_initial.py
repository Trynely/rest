# Generated by Django 4.2.5 on 2024-01-23 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('title', models.CharField(max_length=100, verbose_name='Название Категории')),
                ('img', models.ImageField(upload_to='image/%Y', verbose_name='Изображение')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('text', models.TextField(blank=True, verbose_name='Описание')),
                ('img', models.ImageField(blank=True, upload_to='image/%Y', verbose_name='Изображение')),
                ('size', models.CharField(blank=True, max_length=200, verbose_name='Выбранный размер')),
                ('quantity', models.IntegerField(default=1, verbose_name='Количество')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Цена')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Things',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('text', models.TextField(blank=True, verbose_name='Описание')),
                ('one_img', models.ImageField(blank=True, upload_to='image/%Y', verbose_name='Изображение')),
                ('two_img', models.ImageField(blank=True, upload_to='image/%Y', verbose_name='Изображение')),
                ('made_in', models.TextField(max_length=50, verbose_name='Страна производства')),
                ('size', models.CharField(blank=True, max_length=200, verbose_name='Доступные Размеры')),
                ('quantity', models.IntegerField(default=1, verbose_name='Количество')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Цена')),
                ('available', models.BooleanField(verbose_name='В наличии')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='one.category', verbose_name='Категория')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Вещь',
                'verbose_name_plural': 'Вещи',
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('selected_size', models.IntegerField(verbose_name='Выбранный размер')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='image/%Y', verbose_name='Изображение')),
                ('thing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thing', to='one.things', verbose_name='Для')),
            ],
            options={
                'verbose_name': 'Картинка',
                'verbose_name_plural': 'Картинки',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('text', models.TextField(blank=True, verbose_name='Описание')),
                ('img', models.ImageField(blank=True, upload_to='image/%Y', verbose_name='Изображение')),
                ('size', models.CharField(blank=True, max_length=200, verbose_name='Выбранный размер')),
                ('quantity', models.IntegerField(default=1, verbose_name='Количество')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Цена')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
                'ordering': ['-updated', '-created'],
            },
        ),
    ]
