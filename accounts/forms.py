from django import forms
from django.contrib.auth.models import User
from .models import Profile

INPUT_CLASS = (
    "w-full p-3 rounded-xl border border-dateBrown/30 bg-white text-dateBrown placeholder-dateBrown/40 "
    "focus:border-dateBrown focus:ring-2 focus:ring-palmGold outline-none"
)

class BuyerSellerRegisterForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=[(Profile.ROLE_BUYER, "مشتري"), (Profile.ROLE_SELLER, "بائع")],
        label="نوع الحساب",
        widget=forms.RadioSelect,
        required=True
    )

    name = forms.CharField(
        required=True,
        label="الاسم",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "اكتب الاسم"})
    )

    phone = forms.CharField(
        required=False,
        label="رقم الهاتف (اختياري)",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "05xxxxxxxx"})
    )

    username = forms.CharField(
        required=True,
        label="اسم المستخدم",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "اكتب اسم المستخدم"})
    )

    password = forms.CharField(
        required=True,
        label="كلمة المرور",
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "اكتب كلمة المرور"})
    )

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("اسم المستخدم مستخدم مسبقًا.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["name"]
        user.last_name = ""
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
            profile = user.profile
            profile.role = self.cleaned_data["role"]
            profile.phone = self.cleaned_data.get("phone", "") or ""
            profile.save()

        return user