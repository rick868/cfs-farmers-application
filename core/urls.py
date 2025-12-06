from django.urls import path
from django.urls import path
from .views import AnalyticsView, ChatbotAPIView

urlpatterns = [
    path('reports/', AnalyticsView.as_view(), name='reports'),
    path('api/chat/', ChatbotAPIView.as_view(), name='chatbot_api'),
]
