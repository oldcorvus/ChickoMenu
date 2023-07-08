from django.contrib import admin
from .models import UserPlan, Plan, PlanItem
# Register your models here.

admin.site.register(UserPlan)
admin.site.register(Plan)
admin.site.register(PlanItem)