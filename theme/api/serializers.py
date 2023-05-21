from rest_framework import serializers
from ..models import Theme

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('name', 'description', 'preview', 'background_image', 'font_family', 'menu_background_color', 'menu_text_color')
        read_only_fields = ("id",)