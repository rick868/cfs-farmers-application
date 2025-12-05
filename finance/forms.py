from django import forms
from .models import LoanRequest, InsurancePolicy

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['amount', 'purpose', 'repayment_period']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount in KES'}),
            'purpose': forms.Select(attrs={'class': 'form-control'}),
            'repayment_period': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Months'}),
        }

class InsuranceApplicationForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = ['crop_type', 'acreage', 'coverage_amount']
        widgets = {
            'crop_type': forms.Select(attrs={'class': 'form-control'}),
            'acreage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Acres'}),
            'coverage_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Value in KES'}),
        }
