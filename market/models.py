from django.db import models
from django.conf import settings

class MarketListing(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    crop_name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50, help_text="e.g. 90kg bag")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='market_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} by {self.seller.username}"
