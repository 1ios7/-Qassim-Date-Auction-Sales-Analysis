from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="sales_analysis_home"),
    path("download/", views.download_sales_csv, name="sales_analysis_download"),
]