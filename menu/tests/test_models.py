from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Menu, Category, MenuItem
import decimal
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class MenuItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpass',
        email="testemail@example.com", phone_number="09905150258")
        menu = Menu.objects.create(name='Test Menu', owner=user)
        category = Category.objects.create(menu=menu, name='Test Category')
        MenuItem.objects.create(
            menu=menu,
            id ='f1bedde9-be1e-4f1f-91bb-793a383eaae7',
            category=category,
            name='Test Item',
            description='Test Description',
            price=decimal.Decimal('10.00'),
            discount=decimal.Decimal('0.8'),
            image=SimpleUploadedFile('test_image.jpg', b'content'),
            is_available=True,
        )

    def test_menu_foreign_key(self):
        menu_item = MenuItem.objects.get(id='f1bedde9-be1e-4f1f-91bb-793a383eaae7')
        self.assertEqual(menu_item.menu.name, 'Test Menu')

    def test_category_foreign_key(self):
        menu_item = MenuItem.objects.get(id='f1bedde9-be1e-4f1f-91bb-793a383eaae7')
        self.assertEqual(menu_item.category.name, 'Test Category')

    def test_price_decimal_places(self):
        menu_item = MenuItem.objects.get(id='f1bedde9-be1e-4f1f-91bb-793a383eaae7')
        self.assertEqual(menu_item.price, decimal.Decimal('10.00'))

    def test_menu_item_str_method(self):
        # Test the __str__ method of the MenuItem model
        menu_item = MenuItem.objects.get(id='f1bedde9-be1e-4f1f-91bb-793a383eaae7')
        expected_str = f"{menu_item.category}/{menu_item.name}"
        self.assertEqual(str(menu_item), expected_str)

    def test_menu_item_create_method(self):
        # Test the create method of the MenuItem model
        menu_item = MenuItem.objects.create(
            menu=Menu.objects.get(name='Test Menu'),
            category=Category.objects.get(name='Test Category'),
            name='New Test Item',
            description='New Test Description',
            price=decimal.Decimal('5.00'),
            discount=decimal.Decimal('0.5'),
            image=SimpleUploadedFile('test_image.jpg', b'content'),
            is_available=False,
        )
        self.assertEqual(menu_item.menu.name, 'Test Menu')
        self.assertEqual(menu_item.category.name, 'Test Category')
        self.assertEqual(menu_item.name, 'New Test Item')
        self.assertEqual(menu_item.description, 'New Test Description')
        self.assertEqual(menu_item.price, decimal.Decimal('5.00'))
        self.assertEqual(menu_item.discount, decimal.Decimal('0.5'))
        self.assertFalse(menu_item.is_available)

    def test_menu_item_update_method(self):
        # Test the update method of the MenuItem model
        menu_item = MenuItem.objects.get(id='f1bedde9-be1e-4f1f-91bb-793a383eaae7')
        menu_item.description = 'Updated Test Description'
        menu_item.save()
        updated_menu_item = MenuItem.objects.get(id='f1bedde9-be1e-4f1f-91bb-793a383eaae7')
        self.assertEqual(updated_menu_item.description, 'Updated Test Description')

        
class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass',
        email="testemail@email.com", phone_number="09905150258")
        self.menu = Menu.objects.create(
            owner=self.user,
            name='Test Menu',
            image='test.jpg',
            code=12345
        )

        
    def test_category_creation(self):
        category = Category.objects.create(
            menu=self.menu,
            name='Test Category',
            emoji='🍔'
        )
        self.assertEqual(str(category), f'{self.menu}/{category.name}')

    def test_category_emoji(self):
        category = Category.objects.create(
            menu=self.menu,
            name='Test Category',
            emoji='🍔'
        )
        self.assertEqual(category.emoji, '🍔')

    def test_category_name_max_length(self):
        category = Category.objects.create(
            menu=self.menu,
            name='x' * 255,
            emoji='🍔'
        )
        self.assertEqual(len(category.name), 255)

class MenuItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpass',
        email="testemail@email.com", phone_number="09905150258")
        menu = Menu.objects.create(name='Test Menu' , owner =user )
        category = Category.objects.create(menu=menu, name='Test Category')
        MenuItem.objects.create(
            menu=menu,
            id ='f1bedde9-be1e-4f1f-91bb-793a383eaae7',
            category=category,
            name='Test Item',
            description='Test Description',
            price=decimal.Decimal('10.00'),
            discount=decimal.Decimal('0.8'),
            image=SimpleUploadedFile('test_image.jpg', b'content'),
            is_available=True,
        )

    def test_menu_foreign_key(self):
        menu_item = MenuItem.objects.get(id ='f1bedde9-be1e-4f1f-91bb-793a383eaae7')
        self.assertEqual(menu_item.menu.name, 'Test Menu')

    def test_category_foreign_key(self):
        menu_item = MenuItem.objects.get(id ='f1bedde9-be1e-4f1f-91bb-793a383eaae7')
        self.assertEqual(menu_item.category.name, 'Test Category')

    def test_price_decimal_places(self):
        menu_item = MenuItem.objects.get(id ='f1bedde9-be1e-4f1f-91bb-793a383eaae7')
        self.assertEqual(menu_item.price, decimal.Decimal('10.00'))
