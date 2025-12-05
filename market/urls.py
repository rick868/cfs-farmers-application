from django.urls import path
from .views import MarketplaceView, CreateListingView

urlpatterns = [
    path('', MarketplaceView.as_view(), name='marketplace'),
    path('sell/', CreateListingView.as_view(), name='create_listing'),
]
