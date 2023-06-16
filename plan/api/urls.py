from django.urls import path, include
from rest_framework.routers import DefaultRouter
from plan.api.views import PlanViewSet, PlanItemViewSet, UserPlanCreateAPIView, UserPlansAPIView

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'planitems', PlanItemViewSet, basename='planitem')

app_name = "plan"

urlpatterns = [
    path('', include(router.urls)),
    path('user-plans/create/', UserPlanCreateAPIView.as_view(), name='user_plan_create'),
    path('user-plans/<str:user_id>/', UserPlansAPIView.as_view(), name='user_plans'),
]