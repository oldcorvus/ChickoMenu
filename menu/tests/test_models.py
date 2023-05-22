from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Menu

User = get_user_model()

class MenuModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        cls.test_user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)

        
        # Create a menu for testing
        cls.test_menu = Menu.objects.create(
            owner=cls.test_user,
            name='Test Menu',
            image='/path/to/image.jpg',
            number_of_qrcodes=1,
            code=12345,
            telephone='123-456-7890',
            phone='123-456-7890',
            address='123 Main St',
            is_active=False,
            is_paid=False,
            primary_color='#007bff',
            secondary_color='#6c757d'
        )

    def test_menu_str_method(self):
        # Test the __str__ method of the Menu model
        test_menu = self.test_menu
        expected_str = f"testuser/Test Menu"
        self.assertEqual(str(test_menu), expected_str)

    def test_active_menus_manager(self):
        # Test the ActiveMenuManager manager
        inactive_menu = Menu.objects.create(
            owner=self.test_user,
            name='Inactive Menu',
            image='/path/to/image.jpg',
            is_active= False,
            is_paid=True
        )
        active_menu = Menu.objects.create(
            owner= self.test_user,
            name='Active Menu',
            image='/path/to/image.jpg',
            code = 64326,
            is_active=True,
            is_paid=True
        )
        active_menus = Menu.active_menus.all()
        self.assertIn(active_menu, active_menus)
        self.assertNotIn(inactive_menu, active_menus)

    def test_user_menus_manager(self):
        # Test the UserMenusManager manager
        user = self.test_user
        user_menu = Menu.objects.create(
            owner=user,
            name='User Menu',
            image='/path/to/image.jpg',
            number_of_qrcodes=1,
            code=64321,
            telephone='123-456-7890',
            phone='123-456-7890',
            address='123 Main St',
            is_active=True,
            is_paid=True,
            primary_color='#007bff',
            secondary_color='#6c757d'
        )
        other_user_menu = Menu.objects.create(
            owner=User.objects.create(username="testuser2", first_name="Test", last_name="User",
                                        phone_number="09905150257", email="testuseer@example.com",
                                        is_active=True, is_admin=False, is_staff=False)
,
            name='Other User Menu',
            image='/path/to/image.jpg',
            is_active=True,
            is_paid=True
        )
        user_menus = Menu.user_menus.get_queryset(user)
        self.assertIn(user_menu, user_menus)
        self.assertNotIn(other_user_menu, user_menus)