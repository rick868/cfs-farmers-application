from django.shortcuts import render
from django.views.generic import TemplateView

class AnalyticsView(TemplateView):
    template_name = 'reports.html'
