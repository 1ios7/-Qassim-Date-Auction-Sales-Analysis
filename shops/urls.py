from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="shops_dashboard"),
    path("login/", views.shop_login, name="shops_login"),
    path("register/", views.shop_register, name="shops_register"),
    path("profile/", views.shop_profile_edit, name="shops_profile"),
    path("products/", views.products_list, name="shops_products"),
    path("products/new/", views.product_create, name="shops_product_create"),
    path("products/<int:pk>/edit/", views.product_edit, name="shops_product_edit"),
    path("products/<int:pk>/delete/", views.product_delete, name="shops_product_delete"),
    path("products/<int:pk>/create-auction/", views.product_create_auction, name="shops_product_create_auction"),

    path("all/", views.public_shops_list, name="public_shops_list"),
    path("store/<int:pk>/", views.public_shop_detail, name="public_shop_detail"),
    path("cart/", views.cart_view, name="shops_cart"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="shops_add_to_cart"),
    path("cart/update/<int:pk>/", views.cart_update, name="shops_cart_update"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="shops_cart_remove"),
    path("cart/checkout/", views.checkout, name="shops_checkout"),
]