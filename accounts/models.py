from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_jalali.db import models as jmodels
from .manager import UserManager
from utils.str import get_random_str
from django.urls import reverse
from utils.models import TimeStampedUUIDModel
import uuid
try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _

from plan.models import UserPlan, Plan

def upload_location(instance, filename):
    return f"UserProfiles/{instance.username.lower()}/{get_random_str(10, 50)}.jpg"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = models.CharField(max_length=60, unique=True, db_index=True,
                                verbose_name="نام کاربری")

    first_name = models.CharField(max_length=20,
                                  verbose_name="نام", blank=True)
                                  
    last_name = models.CharField(max_length=30,
                                 verbose_name="نام خانوادگی", blank=True)
    phone_number = models.CharField(max_length=11, unique=True,verbose_name="شماره تماس")
    email = models.EmailField(unique=True, verbose_name="ایمیل شما")
    date_joined = jmodels.jDateTimeField("تاریخ عضویت", default=timezone.now)
    profile_image = models.ImageField(upload_to=upload_location, verbose_name="عکس پروفایل",
                                      null=True, blank=True)
    address = models.TextField(max_length=420, null=True, blank=True, verbose_name=_('address'))
    post_code = models.PositiveBigIntegerField(null=True, blank=True, verbose_name=_('post code'))
    plans = models.ManyToManyField(Plan, through=UserPlan)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number','email']

    def __str__(self):
        return f'{self.username}--{self.phone_number}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = 'پروفايل كاربر'
        verbose_name_plural = 'پروفايل كاربرها'

    def get_absolute_url(self):
        return reverse('accounts:user-profile', args=(self.username,))

    def get_active_plan(self):
        return self.userplan_set.filter(is_active=True).first()

    def activate_plan(self, plan):
        user_plan = UserPlan.objects.get(user=self, plan=plan)
        user_plan.activate()

    def deactivate_active_plan(self):
        active_plan = self.get_active_plan()
        if active_plan:
            active_plan.deactivate()

class SMSVerification(TimeStampedUUIDModel):
    security_code = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=11)
    session_token = models.CharField(max_length=500)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = "sms_verification"
        verbose_name = "SMS Verification"
        verbose_name_plural = "SMS Verifications"
        ordering = ("-modified_at",)
        unique_together = ("security_code", "phone_number", "session_token")


    def __str__(self):
        return f"{self.phone_number}: {self.security_code}"
