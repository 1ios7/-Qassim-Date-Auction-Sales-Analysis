from django.contrib import admin
from .models import Auction, AuctionImage, Bid


class AuctionImageInline(admin.TabularInline):
    model = AuctionImage
    extra = 1


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "start_price", "min_increment", "is_published", "start_time", "end_time")
    list_filter = ("is_published",)
    search_fields = ("title", "seller__username")
    inlines = [AuctionImageInline]


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "bidder", "amount", "created_at")
    list_filter = ("auction",)
    search_fields = ("auction__title", "bidder__username")