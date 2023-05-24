from django.test import TestCase
from ..serializers import MenuItemSerializer
from menu.models import MenuItem, Menu, Category
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
User = get_user_model()


class MenuItemSerializerTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)

        self.menu = Menu.objects.create(name='Test Menu' , owner =user )

        self.category = Category.objects.create(menu=self.menu, name='Test Category')

        self.menu_item_data = {
        'name': 'Pizza',
        'description': 'A delicious pizza',
        'price': '10.99',
        'discount': '0.50',
        'image': 'https://example.com/pizza.jpg',
        'is_available': True,
        'menu': self.menu  ,
        'category': self.category,
        }
        self.menu_item = MenuItem.objects.create(**self.menu_item_data)
        self.serializer = MenuItemSerializer(instance=self.menu_item)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description', 'price', 'discount', 'image', 'is_available', 'menu', 'category'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.menu_item_data['name'])

    def test_price_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['price'], self.menu_item_data['price'])

    def test_discount_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['discount'], self.menu_item_data['discount'])

    def test_menu_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['menu'], self.menu_item_data['menu'].id)

    def test_category_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['category'], self.menu_item_data['category'].id)
