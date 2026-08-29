from decimal import Decimal
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Profile
from auctions.models import Auction, AuctionImage


def _extract_category_and_clean_description(description: str):
    description = (description or "").strip()
    category = ""
    clean_description = description

    if description.startswith("النوع:"):
        parts = description.split("\n\n", 1)
        first_line = parts[0].strip()
        category = first_line.replace("النوع:", "", 1).strip()

        if len(parts) > 1:
            clean_description = parts[1].strip()
        else:
            clean_description = ""

    return category, clean_description


def _build_description(category: str, description: str):
    category = (category or "").strip()
    description = (description or "").strip()

    if category and description:
        return f"النوع: {category}\n\n{description}"
    if category:
        return f"النوع: {category}"
    return description


@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": Profile.ROLE_BUYER, "phone": ""}
    )

    if profile.role != Profile.ROLE_SELLER:
        return redirect("role_redirect")

    seller_auctions = (
        Auction.objects.filter(seller=request.user)
        .prefetch_related("images", "bids")
        .order_by("-created_at")
    )

    now = timezone.now()

    stats = {
        "total": seller_auctions.count(),
        "open": seller_auctions.filter(is_published=True, start_time__lte=now, end_time__gte=now).count(),
        "closed": seller_auctions.filter(end_time__lt=now).count(),
        "suspended": seller_auctions.filter(is_published=False).count(),
        "cancelled": 0,
    }

    return render(
        request,
        "seller/dashboard.html",
        {
            "stats": stats,
            "auctions": seller_auctions,
        },
    )


@login_required
def new_auction(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": Profile.ROLE_BUYER, "phone": ""}
    )

    if profile.role != Profile.ROLE_SELLER:
        return redirect("role_redirect")

    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        category = (request.POST.get("category") or "").strip()
        description = (request.POST.get("description") or "").strip()
        start_price_raw = (request.POST.get("start_price") or "0").strip()
        min_increment_raw = (request.POST.get("min_increment") or "10").strip()
        start_time_raw = (request.POST.get("start_time") or "").strip()
        end_time_raw = (request.POST.get("end_time") or "").strip()

        if not title:
            messages.error(request, "اسم المزاد / المنتج مطلوب.")
            return render(request, "seller/new_auction.html")

        if not end_time_raw:
            messages.error(request, "وقت نهاية المزاد مطلوب.")
            return render(request, "seller/new_auction.html")

        try:
            start_price = Decimal(start_price_raw)
        except Exception:
            messages.error(request, "سعر البداية غير صحيح.")
            return render(request, "seller/new_auction.html")

        try:
            min_increment = Decimal(min_increment_raw)
        except Exception:
            messages.error(request, "قيمة أقل زيادة غير صحيحة.")
            return render(request, "seller/new_auction.html")

        if start_price < 0:
            messages.error(request, "سعر البداية لا يمكن أن يكون أقل من صفر.")
            return render(request, "seller/new_auction.html")

        if min_increment <= 0:
            messages.error(request, "أقل زيادة لازم تكون أكبر من صفر.")
            return render(request, "seller/new_auction.html")

        try:
            end_dt = datetime.fromisoformat(end_time_raw)
            if timezone.is_naive(end_dt):
                end_dt = timezone.make_aware(end_dt, timezone.get_current_timezone())
        except Exception:
            messages.error(request, "وقت نهاية المزاد غير صحيح.")
            return render(request, "seller/new_auction.html")

        if start_time_raw:
            try:
                start_dt = datetime.fromisoformat(start_time_raw)
                if timezone.is_naive(start_dt):
                    start_dt = timezone.make_aware(start_dt, timezone.get_current_timezone())
            except Exception:
                messages.error(request, "وقت بداية المزاد غير صحيح.")
                return render(request, "seller/new_auction.html")
        else:
            start_dt = timezone.now()

        if end_dt <= start_dt:
            messages.error(request, "وقت نهاية المزاد لازم يكون بعد وقت البداية.")
            return render(request, "seller/new_auction.html")

        final_description = _build_description(category, description)

        auction = Auction.objects.create(
            seller=request.user,
            title=title,
            description=final_description,
            start_price=start_price,
            min_increment=min_increment,
            start_time=start_dt,
            end_time=end_dt,
            is_published=True,
        )

        images = request.FILES.getlist("images")
        for image_file in images:
            AuctionImage.objects.create(auction=auction, image=image_file)

        messages.success(request, "تم إضافة المزاد الجديد بنجاح ✅")
        return redirect("seller_dashboard")

    return render(request, "seller/new_auction.html")


@login_required
def edit_auction(request, pk):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": Profile.ROLE_BUYER, "phone": ""}
    )

    if profile.role != Profile.ROLE_SELLER:
        return redirect("role_redirect")

    auction = get_object_or_404(
        Auction.objects.prefetch_related("images"),
        pk=pk,
        seller=request.user
    )

    current_category, current_description = _extract_category_and_clean_description(auction.description)

    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        category = (request.POST.get("category") or "").strip()
        description = (request.POST.get("description") or "").strip()
        start_price_raw = (request.POST.get("start_price") or "0").strip()
        min_increment_raw = (request.POST.get("min_increment") or "10").strip()
        start_time_raw = (request.POST.get("start_time") or "").strip()
        end_time_raw = (request.POST.get("end_time") or "").strip()

        if not title:
            messages.error(request, "اسم المزاد / المنتج مطلوب.")
            return render(
                request,
                "seller/new_auction.html",
                {
                    "auction": auction,
                    "is_edit": True,
                    "auction_category": category,
                    "auction_clean_description": description,
                },
            )

        if not end_time_raw:
            messages.error(request, "وقت نهاية المزاد مطلوب.")
            return render(
                request,
                "seller/new_auction.html",
                {
                    "auction": auction,
                    "is_edit": True,
                    "auction_category": category,
                    "auction_clean_description": description,
                },
            )

        try:
            start_price = Decimal(start_price_raw)
        except Exception:
            messages.error(request, "سعر البداية غير صحيح.")
            return render(
                request,
                "seller/new_auction.html",
                {
                    "auction": auction,
                    "is_edit": True,
                    "auction_category": category,
                    "auction_clean_description": description,
                },
            )

        try:
            min_increment = Decimal(min_increment_raw)
        except Exception:
            messages.error(request, "قيمة أقل زيادة غير صحيحة.")
            return render(
                request,
                "seller/new_auction.html",
                {
                    "auction": auction,
                    "is_edit": True,
                    "auction_category": category,
                    "auction_clean_description": description,
                },
            )

        if start_price < 0:
            messages.error(request, "سعر البداية لا يمكن أن يكون أقل من صفر.")
            return render(
                request,
                "seller/new_auction.html",
                {
                    "auction": auction,
                    "is_edit": True,
                    "auction_category": category,
                    "auction_clean_description": description,
                },
            )

        if min_increment <= 0:
            messages.error(request, "أقل زيادة لازم تكون أكبر من صفر.")
            return render(
                request,
                "seller/new_auction.html",
                {
                    "auction": auction,
                    "is_edit": True,
                    "auction_category": category,
                    "auction_clean_description": description,
                },
            )

        try:
            end_dt = datetime.fromisoformat(end_time_raw)
            if timezone.is_naive(end_dt):
                end_dt = timezone.make_aware(end_dt, timezone.get_current_timezone())
        except Exception:
            messages.error(request, "وقت نهاية المزاد غير صحيح.")
            return render(
                request,
                "seller/new_auction.html",
                {
                    "auction": auction,
                    "is_edit": True,
                    "auction_category": category,
                    "auction_clean_description": description,
                },
            )

        if start_time_raw:
            try:
                start_dt = datetime.fromisoformat(start_time_raw)
                if timezone.is_naive(start_dt):
                    start_dt = timezone.make_aware(start_dt, timezone.get_current_timezone())
            except Exception:
                messages.error(request, "وقت بداية المزاد غير صحيح.")
                return render(
                    request,
                    "seller/new_auction.html",
                    {
                        "auction": auction,
                        "is_edit": True,
                        "auction_category": category,
                        "auction_clean_description": description,
                    },
                )
        else:
            start_dt = auction.start_time

        if end_dt <= start_dt:
            messages.error(request, "وقت نهاية المزاد لازم يكون بعد وقت البداية.")
            return render(
                request,
                "seller/new_auction.html",
                {
                    "auction": auction,
                    "is_edit": True,
                    "auction_category": category,
                    "auction_clean_description": description,
                },
            )

        final_description = _build_description(category, description)

        auction.title = title
        auction.description = final_description
        auction.start_price = start_price
        auction.min_increment = min_increment
        auction.start_time = start_dt
        auction.end_time = end_dt
        auction.save()

        images = request.FILES.getlist("images")
        for image_file in images:
            AuctionImage.objects.create(auction=auction, image=image_file)

        messages.success(request, "تم تحديث المزاد بنجاح ✅")
        return redirect("seller_dashboard")

    return render(
        request,
        "seller/new_auction.html",
        {
            "auction": auction,
            "is_edit": True,
            "auction_category": current_category,
            "auction_clean_description": current_description,
        },
    )


@login_required
def delete_auction(request, pk):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": Profile.ROLE_BUYER, "phone": ""}
    )

    if profile.role != Profile.ROLE_SELLER:
        return redirect("role_redirect")

    auction = get_object_or_404(Auction, pk=pk, seller=request.user)

    if request.method == "POST":
        auction.delete()
        messages.success(request, "تم حذف المزاد بنجاح ✅")
        return redirect("seller_dashboard")

    return redirect("seller_dashboard")