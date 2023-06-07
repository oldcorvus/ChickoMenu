from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from theme.models import Theme
from ..serializers import ThemeSerializer

class ThemeSerializerTest(APITestCase):
    def setUp(self):
        # Create a sample Theme object for testing
        preview = SimpleUploadedFile(name='test_preview.png', content=b'', content_type='image/png')
        background_image = SimpleUploadedFile(name='test_background.png', content=b'', content_type='image/png')
        self.theme = Theme.objects.create(
            name='Test Theme',
            description='A test theme for testing purposes',
            preview=preview,
            background_image=background_image,
            font_family='Times New Roman',
            menu_background_color='#ffffff',
            menu_text_color='#000000',
        )
        self.serializer = ThemeSerializer(instance=self.theme)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([ 'id','name', 'description', 'preview', 'background_image', 'font_family', 'menu_background_color', 'menu_text_color']))

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.theme.name)

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['description'], self.theme.description)

    def test_preview_field_content(self):
        data = self.serializer.data
        self.assertIsNotNone(data['preview'])

    def test_background_image_field_content(self):
        data = self.serializer.data
        self.assertIsNotNone(data['background_image'])

    def test_font_family_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['font_family'], self.theme.font_family)

    def test_menu_background_color_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['menu_background_color'], self.theme.menu_background_color)

    def test_menu_text_color_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['menu_text_color'], self.theme.menu_text_color)