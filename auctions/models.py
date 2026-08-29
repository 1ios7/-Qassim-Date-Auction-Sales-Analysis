from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone


class Auction(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_auctions")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    min_increment = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("10.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()

    is_published = models.BooleanField(default=True)

    is_suspended = models.BooleanField(default=False)
    suspension_reason = models.CharField(max_length=255, blank=True, default="")
    suspension_note = models.TextField(blank=True, default="")

    @property
    def is_open(self) -> bool:
        now = timezone.now()
        return self.is_published and not self.is_suspended and (self.start_time <= now <= self.end_time)

    @property
    def current_price(self):
        top = self.bids.order_by("-amount", "-created_at").first()
        return top.amount if top else self.start_price

    @property
    def last_bid(self):
        return self.bids.order_by("-created_at").first()

    def __str__(self):
        return self.title


class AuctionImage(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="auction_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.auction.title}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_bids")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.bidder.username} - {self.amount} on {self.auction.title}"