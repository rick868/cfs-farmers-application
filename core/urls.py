from django.urls import path
from .views import AnalyticsView

urlpatterns = [
    path('reports/', AnalyticsView.as_view(), name='reports'),
]
