from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView, View, ListView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from .ai_service import get_ai_response
from .forms import (
    FarmerGroupForm,
    FarmerInquiryForm,
    GroupJoinForm,
    SoilTestForm,
    TraceabilityForm,
    YieldLogForm,
)
from .models import FarmerGroup, FarmerInquiry, FollowUpFlag, GroupMembership, SoilTest, TraceabilityRecord, YieldLog


class OfficerRequiredMixin(LoginRequiredMixin):
    """Restrict extension views to extension officers."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if getattr(request.user, "role", "") != "OFFICER":
            messages.error(request, "Extension tools are available to extension officers.")
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


class AnalyticsView(TemplateView):
    template_name = 'reports.html'


class ExtensionPhaseOneView(OfficerRequiredMixin, TemplateView):
    """
    Static page for extension officers to share immediate benefits, schedules,
    contacts, and manual advisories while richer features are built.
    """

    template_name = 'extension/phase1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "bulletins": [
                    {
                        "title": "Weather – Next 7 days",
                        "detail": "Light rains expected; avoid fertilizer application before Thursday.",
                    },
                    {
                        "title": "Pest watch – Fall armyworm",
                        "detail": "Scouting advised for maize blocks; report sightings via hotline or WhatsApp.",
                    },
                    {
                        "title": "Seasonal reminder – Land prep",
                        "detail": "Complete land prep this week; seed delivery support available on request.",
                    },
                ],
                "training_sessions": [
                    {
                        "title": "Platform onboarding + Q&A",
                        "time": "Wednesdays 10:00–11:00 (online)",
                        "link": "https://meet.example.com/extension-onboarding",
                    },
                    {
                        "title": "Field clinic – Soil health basics",
                        "time": "Fridays 09:00–11:30 (county office)",
                        "link": "Call to reserve a slot",
                    },
                ],
                "support_contacts": {
                    "hotline": "+254 700 000 000",
                    "whatsapp": "+254 711 111 111",
                    "email": "support@agri360.example",
                    "hours": "Mon–Fri 08:00–17:30, Sat 09:00–13:00",
                },
                "benefits": [
                    "Timely advisories reduce input waste and prevent losses.",
                    "Market tips and buyer leads help you sell at better prices.",
                    "Clear loan/insurance guidance speeds up approvals and payouts.",
                    "Digital records keep farm info in one place and ready for audits.",
                ],
                "privacy_points": [
                    "Farmer data is used only to serve them; no sharing without consent.",
                    "Access is restricted to authorized extension staff and the farmer.",
                    "Farmers can request corrections or deletion of their records.",
                ],
                "early_wins": [
                    {
                        "title": "Nakuru maize growers",
                        "metric": "+8% yield",
                        "detail": "Applied top-dress after rainfall window from advisory.",
                    },
                    {
                        "title": "Kiambu horticulture group",
                        "metric": "12% better price",
                        "detail": "Timed harvest to weekly buyer bulletin; sold via marketplace.",
                    },
                    {
                        "title": "Soil test pilots",
                        "metric": "-10% fertilizer spend",
                        "detail": "Right-sized inputs from soil test guidance.",
                    },
                ],
            }
        )
        return context


class KnowledgeLibraryView(OfficerRequiredMixin, TemplateView):
    template_name = 'extension/knowledge.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "videos": [
                    {"title": "Maize planting best practices", "length": "6 min", "link": "#"},
                    {"title": "Soil sampling basics", "length": "4 min", "link": "#"},
                    {"title": "Scouting for fall armyworm", "length": "5 min", "link": "#"},
                ],
                "howtos": [
                    {"title": "Top-dress timing after rain", "tag": "Maize"},
                    {"title": "Drip line flushing checklist", "tag": "Horticulture"},
                    {"title": "Safe pesticide mixing", "tag": "All crops"},
                ],
                "success_stories": [
                    {
                        "title": "Irrigation scheduling cut water by 15%",
                        "region": "Embu",
                        "detail": "Used weekly advisories and soil moisture checks.",
                    },
                    {
                        "title": "Beans intercropping improved yield",
                        "region": "Nakuru",
                        "detail": "Rotated maize/beans with residue management.",
                    },
                ],
                "seasonal_calendar": [
                    {"crop": "Maize", "window": "Planting: Feb–Mar; Top-dress: 3-4 weeks after emergence"},
                    {"crop": "Beans", "window": "Planting: Mar–Apr; Pest watch: weekly scouting"},
                    {"crop": "Tea", "window": "Pruning: Jul–Aug; Fertilizer: post-prune"},
                ],
                "languages": ["English", "Swahili"],
            }
        )
        return context


class AskExpertView(FormView):
    template_name = 'extension/ask.html'
    form_class = FarmerInquiryForm
    success_url = '/core/extension/ask/'

    def form_valid(self, form):
        inquiry: FarmerInquiry = form.save(commit=False)
        if self.request.user.is_authenticated:
            inquiry.farmer = self.request.user
        inquiry.save()
        messages.success(
            self.request,
            "Question submitted. An officer will respond via your preferred contact.",
        )
        return super().form_valid(form)


class InquiryListView(OfficerRequiredMixin, ListView):
    template_name = 'extension/inquiries.html'
    model = FarmerInquiry
    paginate_by = 20
    context_object_name = "inquiries"

    def get_queryset(self):
        return FarmerInquiry.objects.order_by("-created_at")


class ExtensionDashboardView(OfficerRequiredMixin, TemplateView):
    template_name = 'extension/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["open_inquiries"] = FarmerInquiry.objects.order_by("-created_at")[:10]
        context["followups"] = FollowUpFlag.objects.order_by("-priority", "due_date")[:10]
        context["loan_insurance_guides"] = [
            {"title": "Loan checklist", "items": ["National ID", "Farm size & crop plan", "Past yield records"]},
            {"title": "Insurance claim steps", "items": ["Report within 72h", "Photos of damage", "Field officer visit"]},
        ]
        context["reminders"] = [
            {"title": "Scouting schedule", "detail": "Weekly pest scouting every Tuesday morning"},
            {"title": "Fertilizer safety", "detail": "Use PPE; avoid application before heavy rain"},
        ]
        context["recent_soil_tests"] = SoilTest.objects.order_by("-created_at")[:5]
        context["recent_yields"] = YieldLog.objects.order_by("-created_at")[:5]
        context["groups"] = FarmerGroup.objects.order_by("-created_at")[:5]
        context["traceability"] = TraceabilityRecord.objects.order_by("-created_at")[:5]
        return context


class SoilTestView(OfficerRequiredMixin, FormView):
    template_name = 'extension/soil.html'
    form_class = SoilTestForm
    success_url = '/core/extension/soil/'

    def form_valid(self, form):
        soil: SoilTest = form.save(commit=False)
        if self.request.user.is_authenticated:
            soil.farmer = self.request.user
        # Simple rule-based recommendation seed
        recs = []
        if soil.ph and soil.ph < 5.5:
            recs.append("Soil is acidic; consider liming before planting.")
        if soil.nitrogen is not None and soil.nitrogen < 20:
            recs.append("Nitrogen low; apply N-rich fertilizer at planting and top-dress.")
        if soil.phosphorus is not None and soil.phosphorus < 15:
            recs.append("Phosphorus low; incorporate P fertilizer at land prep.")
        if soil.potassium is not None and soil.potassium < 120:
            recs.append("Potassium low; add K source to balance nutrients.")
        soil.recommendations = "\n".join(recs) if recs else "Levels look okay; maintain balanced fertilization."
        soil.save()
        messages.success(self.request, "Soil test uploaded. Recommendation drafted.")
        return super().form_valid(form)


class YieldLogView(OfficerRequiredMixin, FormView):
    template_name = 'extension/yield.html'
    form_class = YieldLogForm
    success_url = '/core/extension/yield/'

    def form_valid(self, form):
        y: YieldLog = form.save(commit=False)
        if self.request.user.is_authenticated:
            y.farmer = self.request.user
        y.save()
        messages.success(self.request, "Yield recorded.")
        return super().form_valid(form)


class PriceTrendsView(OfficerRequiredMixin, TemplateView):
    template_name = 'extension/prices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["price_trends"] = [
            {"crop": "Maize", "trend": "Steady", "last_week": 38, "this_week": 39, "action": "Sell gradually"},
            {"crop": "Beans", "trend": "Up", "last_week": 95, "this_week": 102, "action": "Good time to sell"},
            {"crop": "Tomato", "trend": "Down", "last_week": 55, "this_week": 48, "action": "Hold if possible"},
        ]
        context["demand_signals"] = [
            {"buyer": "Nairobi wholesaler", "crop": "Beans", "quantity": "30 MT", "price": "KSh 102/kg"},
            {"buyer": "School feeding program", "crop": "Maize", "quantity": "20 MT", "price": "KSh 39/kg"},
        ]
        return context


class InputCalculatorView(OfficerRequiredMixin, TemplateView):
    template_name = 'extension/calculator.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Simple static calculator presets; real calc could use JS later
        context["presets"] = [
            {"crop": "Maize", "seed_rate": "25 kg/ha", "fertilizer": "DAP 100kg/ha at planting; CAN 100kg/ha top-dress"},
            {"crop": "Beans", "seed_rate": "60 kg/ha", "fertilizer": "DAP 50kg/ha at planting"},
            {"crop": "Tomato", "seed_rate": "150-200 g/ha (nursery)", "fertilizer": "NPK 200kg/ha split"},
        ]
        return context


class FarmerGroupsView(OfficerRequiredMixin, FormView):
    template_name = 'extension/groups.html'
    form_class = FarmerGroupForm
    success_url = '/core/extension/groups/'

    def form_valid(self, form):
        group: FarmerGroup = form.save(commit=False)
        if self.request.user.is_authenticated:
            group.created_by = self.request.user
        group.save()
        # auto join creator
        if self.request.user.is_authenticated:
            GroupMembership.objects.get_or_create(group=group, user=self.request.user, defaults={"role": "LEAD"})
        messages.success(self.request, "Group created.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = FarmerGroup.objects.order_by("-created_at")[:20]
        context["join_form"] = GroupJoinForm()
        return context


class GroupJoinView(OfficerRequiredMixin, FormView):
    template_name = 'extension/groups_join.html'
    form_class = GroupJoinForm
    success_url = '/core/extension/groups/'

    def form_valid(self, form):
        membership: GroupMembership = form.save(commit=False)
        if self.request.user.is_authenticated:
            membership.user = self.request.user
        membership.save()
        messages.success(self.request, "Joined group.")
        return super().form_valid(form)


class FollowUpListView(OfficerRequiredMixin, ListView):
    template_name = 'extension/followups.html'
    model = FollowUpFlag
    paginate_by = 20
    context_object_name = "followups"

    def get_queryset(self):
        return FollowUpFlag.objects.order_by("-priority", "due_date", "-updated_at")


class ComplianceView(OfficerRequiredMixin, TemplateView):
    template_name = 'extension/compliance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gap_checklist"] = [
            "Keep field records of inputs, planting, and harvest dates.",
            "Use certified seed and approved agrochemicals.",
            "Maintain buffer zones away from water sources.",
            "Provide PPE for all chemical applications.",
            "Store chemicals securely and dispose containers safely.",
        ]
        context["organic_steps"] = [
            "Use organic-certified inputs and maintain input records.",
            "Separate organic plots and equipment from conventional.",
            "Implement crop rotations and cover crops for soil health.",
            "No synthetic pesticides/fertilizers; use approved biocontrols.",
            "Keep sales/traceability records for organic lots.",
        ]
        return context


class TraceabilityView(OfficerRequiredMixin, FormView):
    template_name = 'extension/traceability.html'
    form_class = TraceabilityForm
    success_url = '/core/extension/traceability/'

    def form_valid(self, form):
        record: TraceabilityRecord = form.save(commit=False)
        if self.request.user.is_authenticated:
            record.farmer = self.request.user
        record.save()
        messages.success(self.request, "Traceability record created. Share the batch code with buyers.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["records"] = TraceabilityRecord.objects.order_by("-created_at")[:20]
        return context


@method_decorator(csrf_exempt, name='dispatch')
class ChatbotAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            query = data.get('message', '')
            response_text = get_ai_response(query)
            return JsonResponse({'response': response_text})
        except Exception:
            return JsonResponse({'response': 'Error processing request.'}, status=500)
