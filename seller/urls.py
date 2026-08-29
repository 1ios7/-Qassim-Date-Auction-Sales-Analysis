from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="seller_dashboard"),
    path("new-auction/", views.new_auction, name="seller_new_auction"),
    path("auctions/<int:pk>/edit/", views.edit_auction, name="seller_edit_auction"),
    path("auctions/<int:pk>/delete/", views.delete_auction, name="seller_delete_auction"),
]