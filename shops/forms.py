from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile
from .models import ShopProfile, ShopProduct

INPUT_CLASS = (
    "w-full p-3 rounded-xl border border-dateBrown/30 bg-white text-dateBrown "
    "placeholder-dateBrown/40 focus:border-dateBrown focus:ring-2 focus:ring-palmGold outline-none"
)


class ShopRegisterForm(forms.Form):
    username = forms.CharField(
        label="اسم المستخدم",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "اسم المستخدم"}),
    )
    password = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "كلمة المرور"}),
    )
    store_name = forms.CharField(
        label="اسم المتجر",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "اسم المتجر"}),
    )
    owner_name = forms.CharField(
        label="اسم صاحب المتجر",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "اسم صاحب المتجر"}),
    )
    email = forms.EmailField(
        label="البريد الإلكتروني",
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "example@mail.com"}),
    )
    phone = forms.CharField(
        label="رقم الهاتف",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "05xxxxxxxx"}),
    )
    city = forms.CharField(
        label="المدينة",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "مثال: بريدة"}),
    )
    description = forms.CharField(
        label="وصف المتجر",
        required=False,
        widget=forms.Textarea(attrs={"class": INPUT_CLASS, "rows": 4, "placeholder": "نبذة عن المتجر"}),
    )
    logo = forms.ImageField(
        label="شعار المتجر",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": INPUT_CLASS}),
    )

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("اسم المستخدم مستخدم مسبقًا.")
        return username

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("البريد الإلكتروني مستخدم مسبقًا.")
        return email

    def save(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        owner_name = self.cleaned_data["owner_name"]
        email = self.cleaned_data["email"]
        phone = self.cleaned_data["phone"]
        store_name = self.cleaned_data["store_name"]
        city = self.cleaned_data["city"]
        description = self.cleaned_data.get("description", "")
        logo = self.cleaned_data.get("logo")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        user.first_name = owner_name
        user.save()

        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={"phone": phone, "role": Profile.ROLE_SHOP}
        )
        profile.phone = phone
        profile.role = Profile.ROLE_SHOP
        profile.save()

        shop = ShopProfile.objects.create(
            owner=user,
            store_name=store_name,
            owner_name=owner_name,
            email=email,
            phone=phone,
            city=city,
            description=description,
            logo=logo,
        )

        return user, shop


class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = ShopProfile
        fields = ["store_name", "description", "phone", "logo", "banner", "owner_name", "email", "city"]
        widgets = {
            "store_name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "اسم المتجر"}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASS, "rows": 4, "placeholder": "نبذة عن المتجر"}),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "05xxxxxxxx"}),
            "owner_name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "اسم صاحب المتجر"}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "example@mail.com"}),
            "city": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "المدينة"}),
            "logo": forms.ClearableFileInput(attrs={"class": INPUT_CLASS}),
            "banner": forms.ClearableFileInput(attrs={"class": INPUT_CLASS}),
        }


class ShopProductForm(forms.ModelForm):
    class Meta:
        model = ShopProduct
        fields = ["title", "category", "description", "price", "stock", "image", "is_available"]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "اسم المنتج"}),
            "category": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "مثال: سكري / خلاص / برحي"}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASS, "rows": 5, "placeholder": "وصف المنتج"}),
            "price": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "placeholder": "السعر"}),
            "stock": forms.NumberInput(attrs={"class": INPUT_CLASS, "placeholder": "الكمية"}),
            "image": forms.ClearableFileInput(attrs={"class": INPUT_CLASS}),
            "is_available": forms.CheckboxInput(attrs={"class": "h-5 w-5 rounded border-dateBrown/30 text-palmGold focus:ring-palmGold"}),
        }