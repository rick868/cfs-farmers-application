from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, View
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import LoanRequest, InsurancePolicy
from .forms import LoanRequestForm, InsuranceApplicationForm
from .utils import calculate_repayment, calculate_premium

class LoanRequestView(LoginRequiredMixin, CreateView):
    model = LoanRequest
    form_class = LoanRequestForm
    template_name = 'finance/loan_request.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.farmer = self.request.user
        return super().form_valid(form)

class InsuranceApplyView(LoginRequiredMixin, CreateView):
    model = InsurancePolicy
    form_class = InsuranceApplicationForm
    template_name = 'finance/insurance_apply.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.farmer = self.request.user
        # Calculate premium on save for prototype
        calcs = calculate_premium(form.instance.crop_type, form.instance.acreage, form.instance.coverage_amount)
        form.instance.premium_paid = calcs['premium'] # Assuming immediate payment for prototype
        return super().form_valid(form)

class FinancialLiteracyView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/literacy.html'

# API endpoints for calculators (for JS frontend)
class CalculateLoanAPI(View):
    def get(self, request):
        amount = request.GET.get('amount')
        months = request.GET.get('months')
        if not amount or not months:
            return JsonResponse({'error': 'Invalid params'}, status=400)
        
        result = calculate_repayment(amount, months)
        return JsonResponse(result)

class CalculatePremiumAPI(View):
    def get(self, request):
        crop = request.GET.get('crop')
        coverage = request.GET.get('coverage')
        if not crop or not coverage:
            return JsonResponse({'error': 'Invalid params'}, status=400)
            
        result = calculate_premium(crop, 1, coverage) # Acreage doesn't impact rate in this simple formula
        return JsonResponse(result)
