from rest_framework import viewsets
from plan.models import Plan, PlanItem, UserPlan
from plan.api.serializers import PlanSerializer, PlanItemSerializer,UserPlanSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly
from rest_framework import generics, permissions

class PlanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    queryset = Plan.objects.prefetch_related('features').all()
    serializer_class = PlanSerializer

class PlanItemViewSet(viewsets.ModelViewSet):
    permission_classes =  [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    queryset = PlanItem.objects.all()
    serializer_class = PlanItemSerializer



class UserPlanCreateAPIView(generics.CreateAPIView):
    serializer_class = UserPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPlansAPIView(generics.ListAPIView):
    serializer_class = UserPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserPlan.objects.select_related('plan').all()

    def get_queryset(self):
        return UserPlan.objects.filter(user=self.request.user)