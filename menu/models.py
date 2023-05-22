from django.db import models
from utils.models import TimeStampedUUIDModel
from django.contrib.auth import get_user_model
from django.utils import timezone
from theme.models import Theme
User = get_user_model()

class ActiveMenuManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_paid=True, is_active=True)


class UserMenusManager(models.Manager):
    def get_queryset(self, user):
        return super().get_queryset().filter(owner=user)


class Menu(TimeStampedUUIDModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    number_of_qrcodes = models.IntegerField(default=1)
    code = models.PositiveIntegerField(unique=True, default=81413)
    telephone = models.CharField(max_length=25, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    last_time_paid = models.DateTimeField(default=timezone.now)
    primary_color = models.CharField(max_length=7, default='#007bff')
    secondary_color = models.CharField(max_length=7, default='#6c757d')
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()
    active_menus = ActiveMenuManager()
    user_menus = UserMenusManager()

    def __str__(self):
        return f"{self.owner.username}/{self.name}"