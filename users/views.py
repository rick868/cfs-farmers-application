from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
import json

from .forms import CustomUserCreationForm
from core.models import FarmerInquiry, FollowUpFlag
from core.services import get_weather_data, get_market_prices, get_farming_tips, get_officer_stats

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    model = CustomUserCreationForm.Meta.model # Use the model from the form
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == "FARMER":
            context.update({
                'weather': get_weather_data(location=self.request.user.location or "Nairobi"),
                'market_prices': get_market_prices(),
                'farming_tip': get_farming_tips(),
            })
        elif self.request.user.role == "OFFICER":
            inquiry_count = FarmerInquiry.objects.filter(status="NEW").count()
            followup_count = FollowUpFlag.objects.exclude(status="DONE").count()
            context.update({
                'stats': get_officer_stats(),
                'recent_alerts': ["Fall Armyworm detected in Sector 4", "Heavy rains expected next week"],
                'inquiry_count': inquiry_count,
                'followup_count': followup_count,
            })
        return context

class DownloadDataView(LoginRequiredMixin, View):
    def get(self, request):
        user_data = {
            'username': request.user.username,
            'email': request.user.email,
            'role': request.user.role,
            'date_joined': str(request.user.date_joined),
        }
        # Ideally, we would fetch related loans, listings etc. here
        response = HttpResponse(json.dumps(user_data, indent=4), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{request.user.username}_data.json"'
        return response

class PrivacyPolicyView(TemplateView):
    template_name = 'privacy.html'
