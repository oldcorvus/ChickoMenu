from django.urls import path, include
from rest_framework.routers import DefaultRouter
from plan.api.views import PlanViewSet, PlanItemViewSet

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')

app_name = "plan"

urlpatterns = [
    path('', include(router.urls)),
]