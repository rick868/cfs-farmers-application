from django.urls import path

from .views import (
    AnalyticsView,
    AskExpertView,
    ChatbotAPIView,
    ExtensionDashboardView,
    ExtensionPhaseOneView,
    KnowledgeLibraryView,
    FarmerGroupsView,
    GroupJoinView,
    ComplianceView,
    TraceabilityView,
    InputCalculatorView,
    InquiryListView,
    PriceTrendsView,
    SoilTestView,
    YieldLogView,
    FollowUpListView,
)

urlpatterns = [
    path('reports/', AnalyticsView.as_view(), name='reports'),
    path('api/chat/', ChatbotAPIView.as_view(), name='chatbot_api'),
    path('extension/', ExtensionPhaseOneView.as_view(), name='extension_phase1'),
    path('extension/knowledge/', KnowledgeLibraryView.as_view(), name='extension_knowledge'),
    path('extension/ask/', AskExpertView.as_view(), name='extension_ask'),
    path('extension/inquiries/', InquiryListView.as_view(), name='extension_inquiries'),
    path('extension/dashboard/', ExtensionDashboardView.as_view(), name='extension_dashboard'),
    path('extension/soil/', SoilTestView.as_view(), name='extension_soil'),
    path('extension/yield/', YieldLogView.as_view(), name='extension_yield'),
    path('extension/prices/', PriceTrendsView.as_view(), name='extension_prices'),
    path('extension/calculator/', InputCalculatorView.as_view(), name='extension_calculator'),
    path('extension/groups/', FarmerGroupsView.as_view(), name='extension_groups'),
    path('extension/groups/join/', GroupJoinView.as_view(), name='extension_groups_join'),
    path('extension/compliance/', ComplianceView.as_view(), name='extension_compliance'),
    path('extension/traceability/', TraceabilityView.as_view(), name='extension_traceability'),
    path('extension/followups/', FollowUpListView.as_view(), name='extension_followups'),
]
