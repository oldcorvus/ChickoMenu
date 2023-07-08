from rest_framework import serializers
from ..models import Theme

class ThemeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Theme
        fields = ('id','name',  'preview', 'logo_image',\
             'font_family', 'menu_background_color', 'menu_text_color',\
                 'header_image', 'header_color' )

    def update(self, instance, validated_data):
        logo_image = validated_data.pop('logo_image', None)
        preview = validated_data.pop('preview', None)
        header_image = validated_data.pop('header_image', None)
        theme = super().update(instance, validated_data)
        if logo_image:
            theme.logo_image.delete()  # delete previous logo image
            theme.logo_image = logo_image
        if preview:
            theme.preview.delete()  # delete previous preview image
            theme.preview = preview
        if header_image:
            theme.header_image.delete()  # delete previous header image
            theme.header_image = header_image
        theme.save()
        return theme