from ..models import  Order
from rest_framework import serializers
try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _

from plan.api.serializers import UserPlanSerializer

class OrderSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user_plan = UserPlanSerializer(read_only= True)

    class Meta:
        model = Order
        fields = ('id', 'user_plan', 'payable_amount', 'is_paid', 'authority')


