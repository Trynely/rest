from django.urls import path
from django.contrib import admin
from .views import *
from django.urls import reverse
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from django.contrib.auth.views import *
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', home, name='home'),
    path('things/', cache_page(60 * 15)(ThingsView.as_view())),
    path('things/<int:pk>/', ThingsDetailView.as_view()),
    
    path('category/', cache_page(60 * 15)(CategoryView.as_view())),
    path('category/<str:slug>/', CategoryThings),
    
    path('images/', ThingImages), 
    path('images/<int:pk>/', ThingImagesDetail),

    path('cart/', cache_page(60 * 15)(CartView.as_view())),
    path('add-to-cart/<int:pk>/', addToCart),
    path('increase-thing-cart/<int:pk>/', increaseThingCart),
    path('decrease-thing-cart/<int:pk>/', decreaseThingCart),
    path('delete-from-cart/<int:pk>/', deleteFromCart),
    path('clear-cart/', clearCart),

    path('wishlist/', cache_page(60 * 15)(WishlistView.as_view())),
    path('add-to-wishlist/<int:pk>/', addToWishlist),
    path('delete-from-wishlist/<int:pk>/', deleteFromWishlist),
    path('clear-wishlist/', clearWishlist),
]