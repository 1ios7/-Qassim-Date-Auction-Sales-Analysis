from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("register/", views.register, name="accounts_register"),
    path("go/", views.role_redirect, name="role_redirect"),
]