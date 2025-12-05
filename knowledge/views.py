from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PolicyDocument

class PolicyListView(LoginRequiredMixin, ListView):
    model = PolicyDocument
    template_name = 'knowledge/policy_list.html'
    context_object_name = 'policies'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

class ServiceLocatorView(LoginRequiredMixin, TemplateView):
    template_name = 'knowledge/service_locator.html'
