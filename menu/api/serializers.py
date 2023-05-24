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
        fields = ( 'name', 'description', 'price', 'discount', 'image', 'is_available', 'menu', 'category')
        read_only_fields = ('id',)

class CategorySerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ( 'name' ,  'menu', 'menu_items',)
        read_only_fields = ('id',)
