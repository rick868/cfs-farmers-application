from django.urls import path
from .views import SignUpView, DashboardView, CustomLoginView, DownloadDataView, PrivacyPolicyView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('download-data/', DownloadDataView.as_view(), name='download_data'),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
]
