from rest_framework import viewsets
from plan.models import Plan, PlanItem
from plan.api.serializers import PlanSerializer, PlanItemSerializer
from rest_framework.permissions import IsAuthenticated

class PlanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Plan.objects.prefetch_related('features').all()
    serializer_class = PlanSerializer

class PlanItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PlanItem.objects.all()
    serializer_class = PlanItemSerializer