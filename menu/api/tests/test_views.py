from django.test import TestCase, RequestFactory
from menu.models import Menu
from ..views import ListOfAllActiveMenus
from ..serializers import MenuSerializer
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse


User = get_user_model()

class ListOfAllActiveMenusTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)

        self.factory = RequestFactory()
        self.view = ListOfAllActiveMenus.as_view()
        self.menu1 = Menu.objects.create(name="Menu 1", is_active=True,is_paid=True, owner = self.user)
        self.menu2 = Menu.objects.create(name="Menu 2", is_active=True,is_paid=True, owner= self.user,code = 2424)
        self.menu3 = Menu.objects.create(name="Menu 3", is_active=False, owner= self.user, code= 2947)

    def test_get_queryset_returns_only_active_menus(self):
        request = self.factory.get("/menus/active/")
        response = self.view(request)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], self.menu1.name)
        self.assertEqual(response.data[1]["name"], self.menu2.name)

    def test_permission_classes_allow_any(self):
        request = self.factory.get("/")
        response = self.view(request)
        self.assertEqual(response.status_code, 200)


class UserMenusTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)


    def test_get_user_menus(self):
        # Create some menus for the authenticated user
        Menu.objects.create(name='Menu 1', owner=self.user)
        Menu.objects.create(name='Menu 2', owner=self.user, code = 1249)
        Menu.objects.create(name='Other user menu',code =2894,\
             owner=User.objects.create_user(username='otheruser', password='otherpass',phone_number="09981203812", email="testuser2@example.com",))

        # Make a GET request to the user_menus URL
        self.client.force_authenticate(user=self.user, token=self.token)
        url = reverse('menu:user_menus')
        response = self.client.get(url)

        # Ensure the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the response contains only the menus created by the authenticated user
        expected_data = MenuSerializer(Menu.objects.filter(owner=self.user), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_create_user_menu(self):
        # Define the data to create a new menu
        new_menu_data = {
            'name': 'My Menu',
            'image': 'https://example.com/menu.jpg',
            'number_of_qrcodes': 10,
            'code': 13325,
            'telephone': '+123456789',
            'phone': '+123456789',
            'address': '123 Main St',
        }

        # Make a POST request to the user_menus URL with the My Menu data
        url = reverse('menu:user_menus')
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.post(url, new_menu_data)

        # Ensure the response status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure the My Menu was created with the correct owner and code
        new_menu = Menu.objects.get(name='My Menu')
        self.assertEqual(new_menu.owner, self.user)
        self.assertIsNotNone(new_menu.code)

    def test_create_user_menu_without_authentication(self):
        # Define the data to create a new menu
        new_menu_data = {
            'name': 'My Menu',
            'image': 'https://example.com/menu.jpg',
            'number_of_qrcodes': 10,
            'code': 13325,
            'telephone': '+123456789',
            'phone': '+123456789',
            'address': '123 Main St',
        }

        # Make a POST request to the user_menus URL with the My Menu data without authentication
        self.client.logout()
        url = reverse('menu:user_menus')
        response = self.client.post(url, new_menu_data)

        # Ensure the response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Ensure no My Menu was created
        self.assertFalse(Menu.objects.filter(name='My Menu').exists())

    def test_create_user_menu_with_invalid_data(self):
        # Define the data to create a new menu with an invalid name (empty string)
        new_menu_data = {'name': ''}

        # Make a POST request to the user_menus URL with the invalid data
        url = reverse('menu:user_menus')
        self.client.force_authenticate(user=self.user, token=self.token)

        response = self.client.post(url, new_menu_data)

        # Ensure the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Ensure no new menu was created
        self.assertFalse(Menu.objects.filter(name='').exists())

