from rest_framework import serializers
from ..models import Theme

class ThemeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Theme
        fields = ('id','name',  'preview', 'logo_image',\
             'font_family', 'menu_background_color', 'menu_text_color',\
                 'header_image', 'header_color' )
