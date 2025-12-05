from django.urls import path
from .views import PolicyListView, ServiceLocatorView

urlpatterns = [
    path('policies/', PolicyListView.as_view(), name='policy_list'),
    path('locator/', ServiceLocatorView.as_view(), name='service_locator'),
]
