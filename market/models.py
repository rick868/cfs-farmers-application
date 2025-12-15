from django.db import models
from django.conf import settings


class MarketListing(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
    ]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    crop_name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50, help_text="e.g. 90kg bag")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    pickup_point = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='market_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="AVAILABLE")
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchases'
    )
    tracking_note = models.TextField(blank=True)
    purchased_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} by {self.seller.username}"
