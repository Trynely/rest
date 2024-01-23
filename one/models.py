from django.urls import reverse
from django.db import models
from django.conf import settings
from django.utils import timezone

tz = timezone.get_default_timezone()

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    title = models.CharField(verbose_name="Название Категории", max_length=100)
    img = models.ImageField(verbose_name="Изображение", upload_to="image/%Y")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.title


class Things(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    title = models.CharField(verbose_name="Название", max_length=200)
    text = models.TextField(verbose_name="Описание", blank=True)
    one_img = models.ImageField(verbose_name="Изображение", upload_to='image/%Y', blank=True)
    two_img = models.ImageField(verbose_name="Изображение", upload_to='image/%Y', blank=True)
    made_in = models.TextField(verbose_name="Страна производства", max_length=50)
    size = models.CharField(verbose_name="Доступные Размеры", max_length=200, blank=True)
    quantity = models.IntegerField(verbose_name="Количество", default=1)
    price = models.IntegerField(verbose_name="Цена", blank=True, null=True)
    available = models.BooleanField(verbose_name="В наличии")

    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.title

class Images(models.Model): 
    thing = models.ForeignKey(Things, verbose_name='Для', related_name="thing", on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField('Изображение', upload_to='image/%Y', blank=False)

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    title = models.CharField(verbose_name="Название", max_length=200)
    text = models.TextField(verbose_name="Описание", blank=True)
    img = models.ImageField(verbose_name="Изображение", upload_to='image/%Y', blank=True)
    size = models.CharField('Выбранный размер', max_length=200, blank=True)
    quantity = models.IntegerField(verbose_name="Количество", default=1)
    price = models.IntegerField(verbose_name="Цена", blank=True, null=True)

    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return f'{self.user.email} — {self.title}'

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    title = models.CharField(verbose_name="Название", max_length=200)
    text = models.TextField(verbose_name="Описание", blank=True)
    img = models.ImageField(verbose_name="Изображение", upload_to='image/%Y', blank=True)
    size = models.CharField('Выбранный размер', max_length=200, blank=True)
    quantity = models.IntegerField(verbose_name="Количество", default=1)
    price = models.IntegerField(verbose_name="Цена", blank=True, null=True)

    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return f'{self.user.email} — {self.title}'
    
class Purchases(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    title = models.CharField(verbose_name="Название", max_length=200)
    selected_size = models.IntegerField(verbose_name="Выбранный размер")
    price = models.IntegerField(verbose_name="Цена")

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return f'{self.user.email} — {self.title}'