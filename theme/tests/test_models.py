from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Theme

class ThemeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample Theme object for testing
        preview = SimpleUploadedFile(name='test_preview.png', content=b'', content_type='image/png')
        background_image = SimpleUploadedFile(name='test_background.png', content=b'', content_type='image/png')
        theme = Theme.objects.create(
            id = 1,
            name='Test Theme',
            description='A test theme for testing purposes',
            preview=preview,
            background_image=background_image,
            font_family='Times New Roman',
            menu_background_color='#ffffff',
            menu_text_color='#000000',
        )

    def test_theme_name(self):
        theme = Theme.objects.get(id=1)
        expected_name = f"{theme.name}"
        self.assertEqual(expected_name, str(theme))

    def test_theme_description(self):
        theme = Theme.objects.get(id=1)
        expected_description = 'A test theme for testing purposes'
        self.assertEqual(expected_description, theme.description)

    def test_theme_font_family(self):
        theme = Theme.objects.get(id=1)
        expected_font_family = 'Times New Roman'
        self.assertEqual(expected_font_family, theme.font_family)

    def test_theme_menu_background_color(self):
        theme = Theme.objects.get(id=1)
        expected_menu_background_color = '#ffffff'
        self.assertEqual(expected_menu_background_color, theme.menu_background_color)

    def test_theme_menu_text_color(self):
        theme = Theme.objects.get(id=1)
        expected_menu_text_color = '#000000'
        self.assertEqual(expected_menu_text_color, theme.menu_text_color)

    def test_theme_preview_upload_to(self):
        theme = Theme.objects.get(id=1)
        expected_upload_to = 'theme_preview'
        self.assertEqual(expected_upload_to, theme.preview.field.upload_to)

    def test_theme_background_image_upload_to(self):
        theme = Theme.objects.get(id=1)
        expected_upload_to = 'theme_image'
        self.assertEqual(expected_upload_to, theme.background_image.field.upload_to)