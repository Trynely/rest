from django.contrib import admin
from .models import Things, Category, Cart, Wishlist, Images

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category, CategoryAdmin)

class ThingsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Things, ThingsAdmin)

admin.site.register(Images)

admin.site.register(Cart)

admin.site.register(Wishlist)

