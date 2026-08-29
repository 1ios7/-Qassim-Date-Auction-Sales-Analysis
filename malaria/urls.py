from django.urls import path
from . import views

urlpatterns = [
    path("", views.malaria_home, name="malaria_home"),
]