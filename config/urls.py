from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("admin/", admin.site.urls),

    path("malaria/", include("malaria.urls")),
    path("qassim-dashboard/", include("qassim_dashboard.urls")),

    path("accounts/", include("accounts.urls")),
    path("seller/", include("seller.urls")),
    path("shops/", include("shops.urls")),
    path("staff/", include("staffpanel.urls")),

    path("logout/", LogoutView.as_view(next_page="portal_home"), name="logout"),

    path("", include("portal.urls")),
    path("", include("auctions.urls")),
    path("sales-analysis/", include("sales_analysis.urls")),
path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
path("logout/", auth_views.LogoutView.as_view(next_page="portal_home"), name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)