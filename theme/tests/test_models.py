from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Theme

class ThemeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample Theme object for testing
        preview = SimpleUploadedFile(name='test_preview.png', content=b'', content_type='image/png')
        header_image = SimpleUploadedFile(name='test_background.png', content=b'', content_type='image/png')
        logo_image = SimpleUploadedFile(name='test_background.png', content=b'', content_type='image/png')

        theme = Theme.objects.create(
            id = 1,
            name='Test Theme',
            preview=preview,
            header_image=header_image,
            logo_image = logo_image,
            header_color='#343a40',
            font_family='Times New Roman',
            menu_background_color='#ffffff',
            menu_text_color='#000000',
            menu_item_background_color = '#ffffff'
        )

        
    def test_theme_logo_image_upload_to(self):
        theme = Theme.objects.get(id=1)
        expected_upload_to = 'theme_image'
        self.assertEqual(expected_upload_to, theme.logo_image.field.upload_to)

    def test_theme_header_color(self):
        theme = Theme.objects.get(id=1)
        expected_header_color = '#343a40'
        self.assertEqual(expected_header_color, theme.header_color)

    def test_theme_header_image_upload_to(self):
        theme = Theme.objects.get(id=1)
        expected_upload_to = 'theme_image'
        self.assertEqual(expected_upload_to, theme.header_image.field.upload_to)

    def test_theme_name(self):
        theme = Theme.objects.get(id=1)
        expected_name = f"{theme.name}"
        self.assertEqual(expected_name, str(theme))

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

    def test_theme_menu_item_background_color(self):
        theme = Theme.objects.get(id=1)
        expected_menu_item_background_color = '#ffffff'
        self.assertEqual(expected_menu_item_background_color, theme.menu_item_background_color)
