from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
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
            context.update({
                'stats': get_officer_stats(),
                'recent_alerts': ["Fall Armyworm detected in Sector 4", "Heavy rains expected next week"]
            })
        return context
