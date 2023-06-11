from django.db import models
from utils.models import TimeStampedUUIDModel
from django.contrib.auth import get_user_model
from django.utils import timezone
from theme.models import Theme
try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _


User = get_user_model()

class ActiveMenuManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_paid=True, is_active=True)


class UserMenusManager(models.Manager):
    def get_queryset(self, user):
        return super().get_queryset().filter(owner=user)


class Menu(TimeStampedUUIDModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
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



class Category(TimeStampedUUIDModel):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=255)
    emoji = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.menu}/{self.name}'


class MenuItem(TimeStampedUUIDModel):
    menu = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name=_('menu'),
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name=_('category'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('description'),
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_('price'),
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        verbose_name=_('discount'),
    )
    image = models.ImageField(
        upload_to='menu_items/',
        verbose_name=_('image'),
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name=_('is available'),
    )

    class Meta:
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')

    def __str__(self):
        return f'{self.category}/{self.name}'