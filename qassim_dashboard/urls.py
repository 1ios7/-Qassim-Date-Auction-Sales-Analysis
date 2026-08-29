from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="qassim_dashboard_home"),
    path("download/", views.download_report, name="qassim_dashboard_download"),
]