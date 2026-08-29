
from decimal import Decimal
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Profile
from auctions.models import Auction, AuctionImage
from .forms import ShopProfileForm, ShopProductForm, ShopRegisterForm
from .models import ShopProfile, ShopProduct, CartItem



def shop_login(request):
    if request.user.is_authenticated:
        try:
            if request.user.profile.role == Profile.ROLE_SHOP:
                return redirect("shops_dashboard")
        except Exception:
            pass

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={"role": Profile.ROLE_BUYER, "phone": ""}
            )

            if profile.role != Profile.ROLE_SHOP:
                messages.error(request, "هذا الحساب ليس حساب متجر.")
                return redirect("shops_login")

            login(request, user)
            return redirect("shops_dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "shops/login.html", {"form": form})


def shop_register(request):
    if request.user.is_authenticated:
        try:
            if request.user.profile.role == Profile.ROLE_SHOP:
                return redirect("shops_dashboard")
        except Exception:
            pass

    if request.method == "POST":
        form = ShopRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user, shop = form.save()
            login(request, user)
            messages.success(request, "تم إنشاء حساب المتجر بنجاح ✅")
            return redirect("shops_dashboard")
    else:
        form = ShopRegisterForm()

    return render(request, "shops/register.html", {"form": form})


def _get_shop_role_or_redirect(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": Profile.ROLE_BUYER, "phone": ""}
    )

    if profile.role != Profile.ROLE_SHOP:
        return None

    shop_profile, created = ShopProfile.objects.get_or_create(
        owner=request.user,
        defaults={
            "store_name": f"متجر {request.user.first_name or request.user.username}",
            "owner_name": request.user.first_name or "",
            "email": request.user.email or "",
            "phone": profile.phone or "",
            "city": "",
            "description": "",
        }
    )
    return shop_profile


@login_required
def dashboard(request):
    shop_profile = _get_shop_role_or_redirect(request)
    if not shop_profile:
        return redirect("role_redirect")

    products = shop_profile.products.order_by("-created_at")
    available_products = products.filter(is_available=True)

    stats = {
        "products": products.count(),
        "sales": shop_profile.total_sales_amount,
        "visitors": shop_profile.visitors_count,
        "active_now": shop_profile.active_now_count,
        "available_products": available_products.count(),
        "out_of_stock": products.filter(stock=0).count(),
    }

    recent_products = products[:6]

    return render(
        request,
        "shops/dashboard.html",
        {
            "shop_profile": shop_profile,
            "stats": stats,
            "recent_products": recent_products,
        },
    )


@login_required
def shop_profile_edit(request):
    shop_profile = _get_shop_role_or_redirect(request)
    if not shop_profile:
        return redirect("role_redirect")

    if request.method == "POST":
        form = ShopProfileForm(request.POST, request.FILES, instance=shop_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث بيانات المتجر ✅")
            return redirect("shops_profile")
    else:
        form = ShopProfileForm(instance=shop_profile)

    return render(
        request,
        "shops/profile.html",
        {
            "form": form,
            "shop_profile": shop_profile,
        },
    )


@login_required
def products_list(request):
    shop_profile = _get_shop_role_or_redirect(request)
    if not shop_profile:
        return redirect("role_redirect")

    products = shop_profile.products.order_by("-created_at")
    return render(
        request,
        "shops/products_list.html",
        {
            "shop_profile": shop_profile,
            "products": products,
        },
    )


@login_required
def product_create(request):
    shop_profile = _get_shop_role_or_redirect(request)
    if not shop_profile:
        return redirect("role_redirect")

    if request.method == "POST":
        form = ShopProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop_profile
            product.save()
            messages.success(request, "تم إضافة المنتج بنجاح ✅")
            return redirect("shops_products")
    else:
        form = ShopProductForm()

    return render(
        request,
        "shops/product_form.html",
        {
            "form": form,
            "shop_profile": shop_profile,
            "is_edit": False,
        },
    )


@login_required
def product_edit(request, pk):
    shop_profile = _get_shop_role_or_redirect(request)
    if not shop_profile:
        return redirect("role_redirect")

    product = get_object_or_404(ShopProduct, pk=pk, shop=shop_profile)

    if request.method == "POST":
        form = ShopProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل المنتج بنجاح ✅")
            return redirect("shops_products")
    else:
        form = ShopProductForm(instance=product)

    return render(
        request,
        "shops/product_form.html",
        {
            "form": form,
            "shop_profile": shop_profile,
            "product": product,
            "is_edit": True,
        },
    )


@login_required
def product_delete(request, pk):
    shop_profile = _get_shop_role_or_redirect(request)
    if not shop_profile:
        return redirect("role_redirect")

    product = get_object_or_404(ShopProduct, pk=pk, shop=shop_profile)

    if request.method == "POST":
        product.delete()
        messages.success(request, "تم حذف المنتج ✅")
        return redirect("shops_products")

    return redirect("shops_products")



@login_required
def product_create_auction(request, pk):
    shop_profile = _get_shop_role_or_redirect(request)
    if not shop_profile:
        return redirect("role_redirect")

    product = get_object_or_404(ShopProduct, pk=pk, shop=shop_profile)

    if request.method == "POST":
        start_price_raw = (request.POST.get("start_price") or str(product.price)).strip()
        min_increment_raw = (request.POST.get("min_increment") or "10").strip()
        end_time_raw = (request.POST.get("end_time") or "").strip()

        if not end_time_raw:
            messages.error(request, "وقت نهاية المزاد مطلوب.")
            return redirect("shops_products")

        try:
            start_price = Decimal(start_price_raw)
        except Exception:
            messages.error(request, "سعر البداية غير صحيح.")
            return redirect("shops_products")

        try:
            min_increment = Decimal(min_increment_raw)
        except Exception:
            messages.error(request, "أقل زيادة غير صحيحة.")
            return redirect("shops_products")

        try:
            end_dt = datetime.fromisoformat(end_time_raw)
            if timezone.is_naive(end_dt):
                end_dt = timezone.make_aware(end_dt, timezone.get_current_timezone())
        except Exception:
            messages.error(request, "وقت نهاية المزاد غير صحيح.")
            return redirect("shops_products")

        if end_dt <= timezone.now():
            messages.error(request, "وقت نهاية المزاد لازم يكون في المستقبل.")
            return redirect("shops_products")

        category_text = f"النوع: {product.category}\n\n" if product.category else ""
        auction_description = (
            f"{category_text}{product.description}\n\n"
            f"منتج قادم من: {shop_profile.store_name}"
        ).strip()

        auction = Auction.objects.create(
            seller=request.user,
            title=product.title,
            description=auction_description,
            start_price=start_price,
            min_increment=min_increment,
            start_time=timezone.now(),
            end_time=end_dt,
            is_published=True,
        )

        # نقل صورة المنتج إلى صور المزاد
        if product.image:
            AuctionImage.objects.create(
                auction=auction,
                image=product.image.name
            )

        messages.success(request, "تم إنشاء مزاد من المنتج بنجاح ✅")
        return redirect("shops_products")

    return redirect("shops_products")
# =========================
# صفحات المتاجر للمشترين
# =========================

def public_shops_list(request):
    shops = (
        ShopProfile.objects.filter(is_active=True, subscription_active=True)
        .prefetch_related("products")
        .order_by("-created_at")
    )

    return render(
        request,
        "shops/public_shops_list.html",
        {
            "shops": shops,
        },
    )


def public_shop_detail(request, pk):
    shop = get_object_or_404(
        ShopProfile.objects.prefetch_related("products"),
        pk=pk,
        is_active=True,
        subscription_active=True,
    )

    products = shop.products.filter(is_available=True).order_by("-created_at")

    return render(
        request,
        "shops/public_shop_detail.html",
        {
            "shop": shop,
            "products": products,
        },
    )


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(ShopProduct, pk=pk, is_available=True)

    if request.method == "POST":
        quantity_raw = (request.POST.get("quantity") or "1").strip()

        try:
            quantity = int(quantity_raw)
        except Exception:
            quantity = 1

        if quantity < 1:
            quantity = 1

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, "تمت إضافة المنتج إلى السلة ✅")
        return redirect("public_shop_detail", pk=product.shop.pk)

    return redirect("public_shop_detail", pk=product.shop.pk)


@login_required
def cart_view(request):
    cart_items = (
        CartItem.objects.filter(user=request.user)
        .select_related("product", "product__shop")
        .order_by("-created_at")
    )

    grand_total = sum(item.total_price for item in cart_items)

    return render(
        request,
        "shops/cart.html",
        {
            "cart_items": cart_items,
            "grand_total": grand_total,
        },
    )


@login_required
def cart_update(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)

    if request.method == "POST":
        quantity_raw = (request.POST.get("quantity") or "1").strip()

        try:
            quantity = int(quantity_raw)
        except Exception:
            quantity = 1

        if quantity <= 0:
            cart_item.delete()
            messages.success(request, "تم حذف المنتج من السلة ✅")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "تم تحديث الكمية ✅")

    return redirect("shops_cart")


@login_required
def cart_remove(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)

    if request.method == "POST":
        cart_item.delete()
        messages.success(request, "تم حذف المنتج من السلة ✅")

    return redirect("shops_cart")


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related("product")

    if not cart_items.exists():
        messages.error(request, "السلة فارغة.")
        return redirect("shops_cart")

    total_amount = Decimal("0.00")
    for item in cart_items:
        total_amount += item.total_price

    cart_items.delete()
    messages.success(request, f"تم تنفيذ الطلب بنجاح ✅ إجمالي الطلب: {total_amount} ر.س")
    return redirect("shops_cart")