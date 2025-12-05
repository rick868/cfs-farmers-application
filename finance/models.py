from django.db import models
from django.conf import settings

class LoanRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    PURPOSE_CHOICES = [
        ('SEEDS', 'Certified Seeds'),
        ('FERTILIZER', 'Fertilizer & Chemicals'),
        ('EQUIPMENT', 'Farm Equipment'),
        ('LABOR', 'Labor Costs'),
        ('OTHER', 'Other'),
    ]

    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    repayment_period = models.IntegerField(help_text="Repayment period in months")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.id} - {self.farmer.username} ({self.amount})"

class InsurancePolicy(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('PENDING', 'Pending Payment'),
    ]
    CROP_CHOICES = [
        ('MAIZE', 'Maize'),
        ('BEANS', 'Beans'),
        ('TEA', 'Tea'),
        ('COFFEE', 'Coffee'),
    ]

    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='insurance_policies')
    crop_type = models.CharField(max_length=50, choices=CROP_CHOICES)
    acreage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Size of land in acres")
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total value insured")
    premium_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    start_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Policy {self.id} - {self.crop_type} ({self.status})"
