from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')), # Includes login/signup/dashboard paths
    path('accounts/', include('django.contrib.auth.urls')), # For logout, password reset standard views if needed
    path('finance/', include('finance.urls')),
    path('market/', include('market.urls')),
    path('knowledge/', include('knowledge.urls')),
    path('core/', include('core.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # Homepage
]
