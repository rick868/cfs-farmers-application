import random

from django.views.generic import ListView, CreateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone

from .models import MarketListing


class FarmerRequiredMixin(LoginRequiredMixin):
    """Ensure only farmers can perform certain actions."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if getattr(request.user, "role", "") != "FARMER":
            messages.error(request, "Only farmers can create listings.")
            return redirect("marketplace")
        return super().dispatch(request, *args, **kwargs)


class MarketplaceView(ListView):
    model = MarketListing
    template_name = 'market/marketplace.html'
    context_object_name = 'listings'
    ordering = ['-created_at']


class CreateListingView(FarmerRequiredMixin, CreateView):
    model = MarketListing
    fields = ['crop_name', 'quantity', 'price_per_unit', 'location', 'pickup_point', 'image']
    template_name = 'market/create_listing.html'
    success_url = reverse_lazy('marketplace')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ListingDetailView(DetailView):
    model = MarketListing
    template_name = 'market/listing_detail.html'
    context_object_name = 'listing'


class PurchaseListingView(LoginRequiredMixin, View):
    """
    Initiate purchase: capture phone, generate simulated M-Pesa OTP, and store in session.
    """

    def post(self, request, pk):
        listing = get_object_or_404(MarketListing, pk=pk)
        if listing.status != "AVAILABLE":
            messages.error(request, "This listing is no longer available.")
            return redirect("listing_detail", pk=pk)
        phone = request.POST.get("phone")
        if not phone:
            messages.error(request, "Enter a phone number to receive the M-Pesa prompt.")
            return redirect("listing_detail", pk=pk)
        amount = listing.price_per_unit
        otp = f"{random.randint(100000, 999999)}"
        request.session[f"mpesa_otp_{pk}"] = otp
        request.session[f"mpesa_phone_{pk}"] = phone
        request.session[f"mpesa_amount_{pk}"] = str(amount)
        messages.success(
            request,
            f"Simulated M-Pesa STK push sent to {phone} for KES {amount}. Enter the OTP to confirm.",
        )
        # In production, call M-Pesa STK push API here with amount and phone.
        return redirect("listing_detail", pk=pk)


class PurchaseConfirmView(LoginRequiredMixin, View):
    """
    Confirm purchase via OTP. On success, mark listing as processing and assign buyer.
    """

    def post(self, request, pk):
        listing = get_object_or_404(MarketListing, pk=pk)
        if listing.status != "AVAILABLE":
            messages.error(request, "This listing is no longer available.")
            return redirect("listing_detail", pk=pk)
        session_key = f"mpesa_otp_{pk}"
        expected = request.session.get(session_key)
        submitted = request.POST.get("otp")
        if not expected:
            messages.error(request, "Start the purchase to receive an OTP first.")
            return redirect("listing_detail", pk=pk)
        if submitted != expected:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("listing_detail", pk=pk)
        listing.buyer = request.user
        listing.status = "PROCESSING"
        listing.purchased_at = timezone.now()
        listing.tracking_note = "Order received. Awaiting seller confirmation."
        listing.save()
        # cleanup session
        request.session.pop(session_key, None)
        request.session.pop(f"mpesa_phone_{pk}", None)
        messages.success(request, "Purchase confirmed. Track status on this page.")
        return redirect("listing_detail", pk=pk)


class ListingStatusUpdateView(LoginRequiredMixin, View):
    """
    Allow seller (or extension officer) to update listing status and tracking note.
    """

    ALLOWED_STATUSES = {"PROCESSING", "SHIPPED", "DELIVERED"}

    def post(self, request, pk):
        listing = get_object_or_404(MarketListing, pk=pk)
        is_owner = request.user == listing.seller
        is_officer = getattr(request.user, "role", "") == "OFFICER"
        if not (is_owner or is_officer):
            messages.error(request, "You are not allowed to update this listing.")
            return redirect("listing_detail", pk=pk)
        new_status = request.POST.get("status")
        note = request.POST.get("tracking_note", "")
        if new_status not in self.ALLOWED_STATUSES:
            messages.error(request, "Invalid status.")
            return redirect("listing_detail", pk=pk)
        listing.status = new_status
        if note:
            listing.tracking_note = note
        listing.save()
        messages.success(request, "Listing status updated.")
        return redirect("listing_detail", pk=pk)
