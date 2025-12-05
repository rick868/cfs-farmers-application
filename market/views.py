from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import MarketListing

class MarketplaceView(LoginRequiredMixin, ListView):
    model = MarketListing
    template_name = 'market/marketplace.html'
    context_object_name = 'listings'
    ordering = ['-created_at']

class CreateListingView(LoginRequiredMixin, CreateView):
    model = MarketListing
    fields = ['crop_name', 'quantity', 'price_per_unit', 'location', 'image']
    template_name = 'market/create_listing.html'
    success_url = reverse_lazy('marketplace')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
