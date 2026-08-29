from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Profile
from auctions.models import Auction, Bid


SUSPEND_REASONS = {
    "مخالفة الشروط": "مخالفة الشروط",
    "بيانات غير مكتملة": "بيانات غير مكتملة",
    "محتوى غير مناسب": "محتوى غير مناسب",
    "معلومات مضللة": "معلومات مضللة",
    "أخرى": "أخرى",
}


@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": Profile.ROLE_BUYER, "phone": ""}
    )

    if not (request.user.is_staff or request.user.is_superuser or profile.role == Profile.ROLE_STAFF):
        return redirect("role_redirect")

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        auction_id = (request.POST.get("auction_id") or "").strip()

        if auction_id:
            auction = get_object_or_404(Auction, pk=auction_id)

            if action == "suspend":
                reason = (request.POST.get("reason") or "").strip()
                custom_reason = (request.POST.get("custom_reason") or "").strip()

                if not reason:
                    messages.error(request, "اختر سبب التعليق.")
                    return redirect("staff_dashboard")

                final_reason = custom_reason if reason == "أخرى" else reason

                if reason == "أخرى" and not custom_reason:
                    messages.error(request, "اكتب السبب المخصص للتعليق.")
                    return redirect("staff_dashboard")

                auction.is_suspended = True
                auction.is_published = False
                auction.suspension_reason = final_reason
                auction.suspension_note = final_reason
                auction.save()

                messages.success(request, "تم تعليق المزاد بنجاح ✅")
                return redirect("staff_dashboard")

            if action == "unsuspend":
                auction.is_suspended = False
                auction.is_published = True
                auction.suspension_reason = ""
                auction.suspension_note = ""
                auction.save()

                messages.success(request, "تم إلغاء تعليق المزاد ✅")
                return redirect("staff_dashboard")

            if action == "delete":
                auction.delete()
                messages.success(request, "تم حذف المزاد نهائيًا ✅")
                return redirect("staff_dashboard")

    now = timezone.now()

    stats = {
        "users_count": User.objects.count(),
        "auctions_count": Auction.objects.count(),
        "open_auctions_count": Auction.objects.filter(
            is_published=True,
            is_suspended=False,
            start_time__lte=now,
            end_time__gte=now
        ).count(),
        "closed_auctions_count": Auction.objects.filter(
            is_suspended=False,
            end_time__lt=now
        ).count(),
        "suspended_auctions_count": Auction.objects.filter(is_suspended=True).count(),
        "bids_count": Bid.objects.count(),
        "buyers_count": Profile.objects.filter(role=Profile.ROLE_BUYER).count(),
        "sellers_count": Profile.objects.filter(role=Profile.ROLE_SELLER).count(),
        "shops_count": Profile.objects.filter(role=Profile.ROLE_SHOP).count(),
    }

    latest_auctions = (
        Auction.objects.select_related("seller")
        .prefetch_related("bids", "images")
        .order_by("-created_at")[:12]
    )

    return render(
        request,
        "staffpanel/dashboard.html",
        {
            "stats": stats,
            "latest_auctions": latest_auctions,
            "suspend_reasons": SUSPEND_REASONS,
        },
    )