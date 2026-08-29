from django.contrib import admin
from .models import ShopProfile, ShopProduct, CartItem


@admin.register(ShopProfile)
class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ("store_name", "owner", "phone", "subscription_active", "is_active")
    search_fields = ("store_name", "owner__username", "phone")


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ("title", "shop", "price", "stock", "is_available", "created_at")
    list_filter = ("is_available", "category")
    search_fields = ("title", "shop__store_name", "category")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "created_at")
    search_fields = ("user__username", "product__title")