from ..models import  Category, Menu, MenuItem
from rest_framework import serializers
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

class MenuDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
  
    class Meta:
        model = Menu
        fields = ( 'name', 'image', 'number_of_qrcodes', 'categories', 'telephone', 'phone', 'address')
        read_only_fields = ('id','code', 'is_payed', 'is_active', 'owner')

class MenuSerializer(SetCustomErrorMessagesMixin, serializers.ModelSerializer):
    """Serializer for the menu object"""

    class Meta:
        model = Menu
        fields = ('name', 'image')
        read_only_fields = ('id','owner')

        extra_kwargs = {
        'name': {
            'error_messages': {
                'blank': _('Name cannot be blank.'),
            },
        },
        'image': {
            'error_messages': {
                'blank': _('Image cannot be blank.'),
            },
        },
    }

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().update(instance, validated_data)