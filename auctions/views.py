from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Profile
from .forms import BidForm
from .models import Auction, Bid


def home(request):
    latest_auctions = Auction.objects.filter(is_published=True).order_by("-created_at")[:6]
    return render(request, "home.html", {"latest_auctions": latest_auctions})


def auctions_list(request):
    auctions = Auction.objects.filter(is_published=True).order_by("-created_at")
    return render(request, "auctions/list.html", {"auctions": auctions})


def auction_detail(request, pk: int):
    auction = get_object_or_404(Auction, pk=pk, is_published=True)
    bid_form = BidForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "لازم تسجل دخول عشان تزايد.")
            return redirect("login")

        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            amount = bid_form.cleaned_data["amount"]

            with transaction.atomic():
                auction_locked = Auction.objects.select_for_update().get(pk=auction.pk)

                if not auction_locked.is_open:
                    messages.error(request, "المزاد مقفل أو انتهى.")
                    return redirect("auction_detail", pk=auction.pk)

                current = auction_locked.current_price
                min_next = current + auction_locked.min_increment

                if Decimal(amount) < Decimal(min_next):
                    messages.error(request, f"لازم مزايدتك تكون على الأقل {min_next} ريال.")
                    return redirect("auction_detail", pk=auction.pk)

                Bid.objects.create(auction=auction_locked, bidder=request.user, amount=amount)
                messages.success(request, "تمت المزايدة بنجاح ✅")
                return redirect("auction_detail", pk=auction.pk)

    bids = auction.bids.select_related("bidder").all()[:15]
    images = auction.images.all()
    return render(
        request,
        "auctions/detail.html",
        {"auction": auction, "bid_form": bid_form, "bids": bids, "images": images},
    )


def auction_status(request, pk: int):
    auction = get_object_or_404(Auction, pk=pk, is_published=True)
    now = timezone.now()
    ends_in = int(max(0, (auction.end_time - now).total_seconds()))

    top_bids = list(
        auction.bids.select_related("bidder")
        .order_by("-created_at")[:10]
        .values("bidder__username", "amount", "created_at")
    )

    return JsonResponse(
        {
            "auction_id": auction.pk,
            "is_open": auction.is_open,
            "current_price": str(auction.current_price),
            "ends_in_seconds": ends_in,
            "top_bids": top_bids,
        }
    )


def about(request):
    return render(request, "pages/about.html")


@login_required
def account(request):
    if request.method == "POST":
        user = request.user

        username = (request.POST.get("username") or "").strip()
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        password = request.POST.get("password") or ""

        if not username:
            messages.error(request, "اسم المستخدم مطلوب.")
            return redirect("account")

        User = get_user_model()
        if username != user.username and User.objects.filter(username=username).exists():
            messages.error(request, "اسم المستخدم مستخدم مسبقًا.")
            return redirect("account")

        user.username = username
        user.email = email

        if name:
            parts = name.split()
            user.first_name = parts[0]
            user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        else:
            user.first_name = ""
            user.last_name = ""

        password_changed = False
        if password.strip():
            user.set_password(password.strip())
            password_changed = True

        user.save()

        try:
            profile = user.profile
        except Exception:
            profile = None

        if profile is None:
            Profile.objects.create(user=user, phone=phone or "")
        else:
            profile.phone = phone or ""
            profile.save()

        if password_changed:
            update_session_auth_hash(request, user)

        messages.success(request, "تم تحديث بيانات حسابك ✅")
        return redirect("account")

    my_bids = request.user.my_bids.select_related("auction").all()[:20]
    return render(request, "pages/account.html", {"my_bids": my_bids})


def landing(request):
    return render(request, "landing.html")