from ..models import  Category, Menu, MenuItem
from rest_framework import serializers
from utils.mixins import SetCustomErrorMessagesMixin
try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _


class MenuItemSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'description', 'price', 'discount', 'image', 'is_available', 'menu', 'category')

class CategorySerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    number_of_items = serializers.SerializerMethodField()
    id = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ( 'id','name' ,  'menu', 'menu_items','number_of_items')

    def get_number_of_items(self, obj):
        return obj.menu_items.count()

class MenuDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField()
    code  = serializers.ReadOnlyField()
    is_payed = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Menu
        fields = ( 'id','owner','code','is_payed','is_active','name', 'image', 'number_of_qrcodes', 'categories', 'telephone', 'phone', 'address')

class MenuSerializer(SetCustomErrorMessagesMixin, serializers.ModelSerializer):
    """Serializer for the menu object"""
    number_of_categories = serializers.SerializerMethodField()
    number_of_items = serializers.SerializerMethodField()
    id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField()

    class Meta:
        model = Menu
        fields = ('id','owner',' name', 'image' , 'number_of_items' , 'number_of_categories')
        

        extra_kwargs = {
        'name': {
            'error_messages': {
                'blank': _('Name cannot be blank.'),
            },
        },
        'image': {   
            'required': False,
            'error_messages': {
                'blank': _('Image cannot be blank.'),
            },
        },
    }
    def get_number_of_categories(self, obj):
        return obj.categories.count()
        
    def get_number_of_items(self, obj):
        categories = obj.categories.all()
        return  sum(category.menu_items.count() for category in categories)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().update(instance, validated_data)