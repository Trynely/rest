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
    path('things/', cache_page(60 * 5, key_prefix="things")(ThingsView.as_view())),
    path('things/<int:pk>/', ThingsDetailView.as_view()),
    
    path('category/', cache_page(60 * 5, key_prefix="categories")(CategoryView.as_view())),
    path('category/<str:slug>/', cache_page(60 * 5, key_prefix="category_things")(CategoryThings)),
    
    path('images/', ThingImages),
    path('images/<int:pk>/', ThingImagesDetail),

    path('cart/', CartView.as_view()),
    path('add-to-cart/<int:pk>/', addToCart),
    path('increase-thing-cart/<int:pk>/', increaseThingCart),
    path('decrease-thing-cart/<int:pk>/', decreaseThingCart),
    path('delete-from-cart/<int:pk>/', deleteFromCart),
    path('clear-cart/', clearCart),

    path('wishlist/', WishlistView.as_view()),
    path('add-to-wishlist/<int:pk>/', addToWishlist),
    path('delete-from-wishlist/<int:pk>/', deleteFromWishlist),
    path('clear-wishlist/', clearWishlist),

    path('filter-min-things/<str:slug>/', FilterMinThings),
    path('filter-max-things/<str:slug>/', FilterMaxThings),
    path('search-things/<str:slug>/', SearchThings),

    path('purchases/', purchases),
    path('add-to-purchases/', addPurchase),
]