from ..models import  Category, MenuItem
from rest_framework import serializers
from rest_framework.validators import  BaseUniqueForValidator
from utils.mixins import SetCustomErrorMessagesMixin
try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'description', 'price', 'discount', 'image', 'is_available', 'menu', 'category')

