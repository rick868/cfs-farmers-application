from django import forms

from .models import (
    FarmerGroup,
    FarmerInquiry,
    GroupMembership,
    SoilTest,
    TraceabilityRecord,
    YieldLog,
)


class FarmerInquiryForm(forms.ModelForm):
    class Meta:
        model = FarmerInquiry
        fields = [
            "name",
            "location",
            "crop",
            "question",
            "preferred_contact",
            "contact_value",
            "preferred_language",
        ]
        widgets = {
            "question": forms.Textarea(attrs={"rows": 4}),
        }


class SoilTestForm(forms.ModelForm):
    class Meta:
        model = SoilTest
        fields = [
            "sample_label",
            "location",
            "crop",
            "file_upload",
            "ph",
            "nitrogen",
            "phosphorus",
            "potassium",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class YieldLogForm(forms.ModelForm):
    class Meta:
        model = YieldLog
        fields = [
            "crop",
            "area_acres",
            "yield_qty",
            "season",
            "region",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class FarmerGroupForm(forms.ModelForm):
    class Meta:
        model = FarmerGroup
        fields = ["name", "region", "purpose", "contact_phone"]


class GroupJoinForm(forms.ModelForm):
    class Meta:
        model = GroupMembership
        fields = ["group", "role"]


class TraceabilityForm(forms.ModelForm):
    class Meta:
        model = TraceabilityRecord
        fields = ["crop", "batch_code", "location", "description", "harvest_date"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

