from django.urls import path
from . import views

urlpatterns = [
    path("auction-landing/", views.landing, name="auction_landing"),
    path("home/", views.home, name="home"),
    path("auctions/", views.auctions_list, name="auctions_list"),
    path("auctions/<int:pk>/", views.auction_detail, name="auction_detail"),
    path("auctions/<int:pk>/status/", views.auction_status, name="auction_status"),
    path("about/", views.about, name="about"),
    path("account/", views.account, name="account"),
]