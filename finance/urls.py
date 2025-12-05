from django.urls import path
from .views import LoanRequestView, InsuranceApplyView, FinancialLiteracyView, CalculateLoanAPI, CalculatePremiumAPI

urlpatterns = [
    path('loan/request/', LoanRequestView.as_view(), name='loan_request'),
    path('insurance/apply/', InsuranceApplyView.as_view(), name='insurance_apply'),
    path('literacy/', FinancialLiteracyView.as_view(), name='financial_literacy'),
    
    # APIs
    path('api/calc-loan/', CalculateLoanAPI.as_view(), name='api_calc_loan'),
    path('api/calc-premium/', CalculatePremiumAPI.as_view(), name='api_calc_premium'),
]
