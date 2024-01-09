from django.forms import ValidationError
from .models import Cart, Category, Things, Wishlist, Images
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from users.models import *

class ThingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Things
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'title', 'text', 'img', 'price', 'quantity', 'updated', 'created')

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'title', 'text', 'img', 'price', 'quantity', 'updated', 'created')
