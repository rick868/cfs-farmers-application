from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .ai_service import get_ai_response

class AnalyticsView(TemplateView):
    template_name = 'reports.html'

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            query = data.get('message', '')
            response_text = get_ai_response(query)
            return JsonResponse({'response': response_text})
        except Exception as e:
            return JsonResponse({'response': 'Error processing request.'}, status=500)
