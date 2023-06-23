from django.test import TestCase
from ..serializers import MenuItemSerializer,MenuDetailSerializer,\
    MenuSerializer, CategorySerializer
from menu.models import MenuItem, Menu, Category
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _
from theme.models import Theme

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

class CategorySerializerTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)

        self.menu = Menu.objects.create(name='Test Menu' , owner =user )

        self.category_data = {
        'name': 'Pizza',
        'menu': self.menu,
        }
        self.category = Category.objects.create(**self.category_data)

        self.menu_item_data = {
        'name': 'Margherita',
        'description': 'A delicious margherita pizza',
        'price': 10.99,
        'discount': 0.5,
        'image': 'https://example.com/margherita.jpg',
        'is_available': True,
        'menu': self.menu,
        'category': self.category,
        }
        self.menu_item = MenuItem.objects.create(**self.menu_item_data)
        self.serializer = CategorySerializer(instance=self.category)
        self.menu_item_serializer = MenuItemSerializer(instance=self.menu_item)


    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.category_data['name'])

    def test_menu_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['menu'], self.category_data['menu'].id)

class MenuDetailSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)
        self.menu_data = {
            'owner': self.user,
            'name': 'My Menu',
            'description': 'My Menu Description',
            'image': 'https://example.com/menu.jpg',
            'number_of_qrcodes': 10,
            'code': 13325,
            'telephone': '+123456789',
            'phone': '+123456789',
            'address': '123 Main St',
        }
        self.menu = Menu.objects.create(**self.menu_data)
        self.category_data = {
            'name': 'Pizza',
            'menu': self.menu,
        }
        self.category = Category.objects.create(**self.category_data)
        self.serializer = MenuDetailSerializer(instance=self.menu)
        self.category_serializer = CategorySerializer(instance=self.category)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'theme', 'description', 'owner', 'code', 'is_paid', 'is_active', 'name', 'image', 'number_of_qrcodes', 'telephone', 'phone', 'address', 'categories'])
        self.assertEqual(data['name'], self.menu_data['name'])
        self.assertEqual(data['description'], self.menu_data['description'])
    
    def test_update_menu_with_theme(self):
        data = {'name': 'Updated Menu', 'theme': { 'name': 'Updated Theme', 'header_color': 'red'}}
        updated_menu = self.serializer.update(self.menu, data)
        self.assertEqual(updated_menu.name, data['name'])
        self.assertEqual(updated_menu.theme.name, 'Updated Theme')
        self.assertEqual(updated_menu.theme.header_color, 'red')
        data = {'name': 'Updated Menu', 'theme': { 'name': 'Updated2 Theme', 'header_color': 'red'}}
        updated_menu = self.serializer.update(self.menu, data)
        self.assertEqual(updated_menu.name, data['name'])
        self.assertEqual(updated_menu.theme.name, 'Updated2 Theme')

        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(Theme.objects.count(), 1)

        
class MenuSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)
 
        self.menu_data = {
            'name': 'My Menu',
            'image': 'https://example.com/menu.jpg',
            'owner' : self.user,
        }
        self.menu = Menu.objects.create(**self.menu_data)

        self.serializer = MenuSerializer(data=self.menu_data, context={'request': {'user': self.user}})

    def test_serializer_with_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serializer_with_blank_name_field(self):
        self.menu_data['name'] = ''
        
        serializer = MenuSerializer(data=self.menu_data)
        expected_error_message = {'name': [_('Name cannot be blank.')]}

        serializer = MenuSerializer(data={'name': ''})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        error_message = str(context.exception.detail['name'][0])

        self.assertEqual(error_message, expected_error_message['name'][0])
    
    def test_update_menu_with_theme(self):
        theme_data = {'name': 'Test Theme', 'header_color': 'blue'}
        theme = Theme.objects.create(**theme_data)
        self.menu.theme = theme
        self.menu.save()
        data = {'name': 'Updated Menu', 'theme': { 'name': 'Updated Theme', 'header_color': 'red'}}
        updated_menu = self.serializer.update(self.menu, data)
        self.assertEqual(updated_menu.name, data['name'])
        self.assertEqual(updated_menu.theme.name,'Updated Theme')
        self.assertEqual(updated_menu.theme.header_color,'red' )
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(Theme.objects.count(), 1)

    def test_update_menu_without_theme(self):
        data = {'name': 'Updated Menu'}

        updated_menu = self.serializer.update(self.menu, data)

        self.assertEqual(updated_menu.name, data['name'])
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(Theme.objects.count(), 0)