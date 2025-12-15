from django.urls import path
from .views import (
    MarketplaceView,
    CreateListingView,
    ListingDetailView,
    ListingStatusUpdateView,
    PurchaseListingView,
    PurchaseConfirmView,
)

urlpatterns = [
    path('', MarketplaceView.as_view(), name='marketplace'),
    path('sell/', CreateListingView.as_view(), name='create_listing'),
    path('listing/<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
    path('listing/<int:pk>/purchase/', PurchaseListingView.as_view(), name='listing_purchase'),
    path('listing/<int:pk>/confirm/', PurchaseConfirmView.as_view(), name='listing_confirm'),
    path('listing/<int:pk>/status/', ListingStatusUpdateView.as_view(), name='listing_status_update'),
]
