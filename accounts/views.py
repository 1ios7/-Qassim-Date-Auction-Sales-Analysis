from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import BuyerSellerRegisterForm
from .models import Profile


def landing(request):
    return render(request, "accounts/landing.html")


def register(request):
    if request.method == "POST":
        form = BuyerSellerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("role_redirect")
    else:
        form = BuyerSellerRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def role_redirect(request):
    # توجيه بعد تسجيل الدخول حسب الدور
    role = getattr(request.user.profile, "role", Profile.ROLE_BUYER)

    if role == Profile.ROLE_SELLER:
        return redirect("seller_dashboard")

    if role == Profile.ROLE_SHOP:
        return redirect("shops_dashboard")

    if role == Profile.ROLE_STAFF:
        return redirect("staff_dashboard")

    # buyer
    return redirect("home")  # صفحة المشتري (من auctions)