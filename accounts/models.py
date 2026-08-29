from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_BUYER = "buyer"
    ROLE_SELLER = "seller"
    ROLE_SHOP = "shop"
    ROLE_STAFF = "staff"

    ROLE_CHOICES = [
        (ROLE_BUYER, "مشتري"),
        (ROLE_SELLER, "بائع"),
        (ROLE_SHOP, "متجر"),
        (ROLE_STAFF, "مشرف"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_BUYER)
    phone = models.CharField(max_length=20, blank=True, default="")

    def __str__(self):
        return f"{self.user.username} ({self.role})"