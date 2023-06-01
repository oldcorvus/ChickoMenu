from django.db import models
from django.utils import timezone
from django.conf import settings


class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.ManyToManyField('PlanItem')

    def __str__(self):
        return self.name

class PlanItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def activate(self):
        active_plan = self.user.userplan_set.filter(is_active=True).first()
        if active_plan:
            active_plan.deactivate()
        self.is_active = True
        self.end_date = None
        self.save()

    def deactivate(self):
        self.is_active = False
        self.end_date = timezone.now()
        self.save()

    class Meta:
        unique_together = ('user', 'plan')
