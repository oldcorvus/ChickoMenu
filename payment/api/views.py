from rest_framework import generics, status, permissions
from rest_framework.response import Response
from payment.models import Order
from .serializers import OrderSerializer
from plan.models import UserPlan
from .permissions import IsUserPlanOwner

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _

class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserPlanOwner]
    queryset = Order.objects.all() 


class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        # Get the user plan with the given id and is_active=True
        user_plan_id = request.data.get('user_plan_id')  # Assuming you are passing user_plan_id in the request data
        try:
            user_plan = UserPlan.objects.get(id=user_plan_id, user=request.user)
        
        except UserPlan.DoesNotExist:
            return Response({"error": _("No active plan found for this user.")}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new order for the active user plan
        order = Order.objects.create(
            user_plan=user_plan,
            payable_amount=user_plan.plan.price
        )

        if user_plan.plan.name == 'Free':
            order.is_paid = True
            order.save()
            user_plan.is_active = True
            user_plan.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        # Get all orders for the current user
        return Order.objects.filter(user_plan__user=self.request.user)



    