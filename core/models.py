from django.conf import settings
from django.db import models


class FarmerInquiry(models.Model):
    CONTACT_CHOICES = [
        ("WHATSAPP", "WhatsApp"),
        ("SMS", "SMS"),
        ("CALL", "Phone call"),
        ("EMAIL", "Email"),
    ]
    STATUS_CHOICES = [
        ("NEW", "New"),
        ("IN_PROGRESS", "In progress"),
        ("ANSWERED", "Answered"),
    ]

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="inquiries"
    )
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    crop = models.CharField(max_length=120, blank=True)
    question = models.TextField()
    preferred_contact = models.CharField(max_length=20, choices=CONTACT_CHOICES, default="WHATSAPP")
    contact_value = models.CharField(max_length=120)
    preferred_language = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NEW")
    response_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.question[:40]}..."


class FollowUpFlag(models.Model):
    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("SCHEDULED", "Scheduled"),
        ("DONE", "Done"),
    ]

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followups"
    )
    topic = models.CharField(max_length=140)
    note = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="MEDIUM")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="OPEN")
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.farmer} - {self.topic}"


class SoilTest(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="soil_tests"
    )
    sample_label = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    crop = models.CharField(max_length=120, blank=True)
    file_upload = models.FileField(upload_to="soil_tests/", blank=True, null=True)
    ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    nitrogen = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="ppm")
    phosphorus = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="ppm")
    potassium = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="ppm")
    notes = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Soil test {self.sample_label}"


class YieldLog(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="yield_logs"
    )
    crop = models.CharField(max_length=120)
    area_acres = models.DecimalField(max_digits=6, decimal_places=2)
    yield_qty = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total harvested (e.g., kg)")
    season = models.CharField(max_length=120, help_text="e.g., 2025 long rains")
    region = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop} - {self.season}"


class FarmerGroup(models.Model):
    name = models.CharField(max_length=140)
    region = models.CharField(max_length=120, blank=True)
    purpose = models.CharField(max_length=180, blank=True)
    contact_phone = models.CharField(max_length=40, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="groups_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    ROLE_CHOICES = [("LEAD", "Lead"), ("MEMBER", "Member")]
    group = models.ForeignKey(FarmerGroup, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="group_memberships")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="MEMBER")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("group", "user")

    def __str__(self):
        return f"{self.user} in {self.group}"


class TraceabilityRecord(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="traceability_records"
    )
    crop = models.CharField(max_length=120)
    batch_code = models.CharField(max_length=64, unique=True)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    harvest_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop} - {self.batch_code}"
