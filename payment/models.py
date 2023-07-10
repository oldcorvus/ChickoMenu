from django.db import models
from plan.models import UserPlan
from utils.models import TimeStampedUUIDModel

class Order(TimeStampedUUIDModel):
    user_plan = models.ForeignKey(UserPlan, on_delete=models.CASCADE)
    payable_amount = models.DecimalField(max_digits=10, decimal_places=2,default= 0.00) 
    is_paid = models.BooleanField(default=False)
    authority = models.CharField(null=True, blank=True, max_length=36)