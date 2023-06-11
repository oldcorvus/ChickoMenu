from django.test import TestCase, RequestFactory
from menu.models import Menu,Category, MenuItem
from ..views import ListOfAllActiveMenus
from ..serializers import MenuSerializer,CategorySerializer,MenuDetailSerializer,MenuItemSerializer
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
            'owner': self.user,
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



class MenuDetailTestCase(APITestCase):
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
        self.token = Token.objects.create(user=self.user)

        self.menu = Menu.objects.create(**self.menu_data)

    def test_get_menu_detail(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user, token = self.token)

        # Make a GET request to the menu detail URL
        url = reverse('menu:menu_detail', args=[self.menu.pk])
        response = self.client.get(url)

        # Ensure the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the response data matches the serialized menu instance
        serializer = MenuDetailSerializer(instance=self.menu)
        self.assertEqual(response.data, serializer.data)

        # Ensure the response data includes the description field
        self.assertIn('description', response.data)
        self.assertEqual(response.data['description'], self.menu_data['description'])

    def test_update_menu_detail(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user, token = self.token)

        # Define the data to update the menu
        updated_data = {'name': 'New Name', 'image':"new.jpg"}

        # Make a PUT request to the menu detail URL
        url = reverse('menu:menu_detail', args=[self.menu.pk])
        response = self.client.put(url, updated_data)

        # Ensure the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the menu instance from the database
        self.menu.refresh_from_db()

        # Ensure the menu instance was updated with the new data
        self.assertEqual(self.menu.name, updated_data['name'])

    def test_delete_menu_detail(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user, token = self.token)

        # Make a DELETE request to the menu detail URL
        url = reverse('menu:menu_detail', args=[self.menu.pk])
        response = self.client.delete(url)

        # Ensure the response status code is 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the menu instance was deleted
        self.assertFalse(Menu.objects.filter(pk=self.menu.pk).exists())

    def test_get_menu_detail_unauthenticated(self):
        # Make a GET request to the menu detail URL without authentication
        url = reverse('menu:menu_detail', args=[self.menu.pk])
        response = self.client.get(url)

        # Ensure the response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_menu_detail_unauthenticated(self):
        # Define the data to update the menu
        updated_data = {'name': 'New Name'}

        # Make a PUT request to the menu detail URL without authentication
        url = reverse('menu:menu_detail', args=[self.menu.pk])
        response = self.client.put(url, updated_data)

        # Ensure the response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Refresh the menu instance from the database
        self.menu.refresh_from_db()

        # Ensure the menu instance was not updated with the new data
        self.assertNotEqual(self.menu.name, updated_data['name'])

    def test_delete_menu_detail_unauthenticated(self):
        # Make a DELETE request to the menu detail URL without authentication
        url = reverse('menu:menu_detail', args=[self.menu.pk])
        response = self.client.delete(url)

        # Ensure the response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Ensure the menu instance was not deleted
        self.assertTrue(Menu.objects.filter(pk=self.menu.pk).exists())
        
class CategoryDetailTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)
        self.user2 = User.objects.create(username="testuser2", first_name="Test", last_name="User",
                                        phone_number="1234678490", email="testuser2@example.com",
                                        is_active=True, is_admin=False, is_staff=False)
        self.token = Token.objects.create(user=self.user1)
        self.menu1 = Menu.objects.create(name='Test Menu 1', owner=self.user1)
        self.menu2 = Menu.objects.create(name='Test Menu 2', owner=self.user2 ,code =235)
        self.category1 = Category.objects.create(name='Category 1', menu=self.menu1)
        self.category2 = Category.objects.create(name='Category 2', menu=self.menu2)

    def test_retrieve_category(self):
        # Test that an authenticated user can retrieve a category from their own menu
        url = reverse('menu:category-detail', kwargs={'pk': self.category1.pk})
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CategorySerializer(self.category1).data)

        # Test that an unauthenticated user cannot retrieve a category
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_category(self):
        # Test that an authenticated user can update a category in their own menu
        url = reverse('menu:category-detail', kwargs={'pk': self.category1.pk})
        data = {'name': 'Updated Category 1','category_pk':self.category1.pk}
        self.client.force_authenticate(self.user1, token= self.token)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, data['name'])

        # Test that an authenticated user cannot update a category in another user's menu
        url = reverse('menu:category-detail', kwargs={'pk': self.category2.pk})
        data = {'name': 'Updated Category 2', 'category_pk':self.category2.pk}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.category2.refresh_from_db()
        self.assertNotEqual(self.category2.name, data['name'])

        # Test that an unauthenticated user cannot update a category

        self.client.logout()
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.category1.refresh_from_db()
        self.assertNotEqual(self.category1.name, data['name'])

    def test_delete_category(self):
        # Test that an authenticated user can delete a category from their own menu
        url = reverse('menu:category-detail', kwargs={'pk': self.category1.pk})
        self.client.force_authenticate(self.user1,token= self.token)
        response = self.client.delete(url, data ={'category_pk':self.category1.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category1.pk).exists())

        # Test that an authenticated user cannot delete a category from another user's menu
        url = reverse('menu:category-detail', kwargs={'pk': self.category2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Category.objects.filter(pk=self.category2.pk).exists())

        # Test that an unauthenticated user cannot delete a category
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Category.objects.filter(pk=self.category2.pk).exists())





class MenuItemDetailTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)
        self.menu = Menu.objects.create(name='Test Menu 1', owner=self.user)
        self.category = Category.objects.create(name='Category 1', menu=self.menu)
        self.menu_item = MenuItem.objects.create(pk= 'd0c9db05-8135-43c6-83d5-a4dd1d2f3fdd',name='Test Item',menu=self.menu, category = self.category, description='Test Description', price=10.0)
        self.url = reverse('menu:menu-item-detail', kwargs={'pk': self.menu_item.pk})
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user, token= self.token)

    def test_retrieve_menu_item(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = MenuItemSerializer(self.menu_item).data
        # Convert the UUID object to a string in the response data
        response_data = response.data
        response_data['id'] = str(response_data['id'])
        self.assertEqual(response.data, expected_data)

    def test_update_menu_item(self):
        data = {'name': 'Updated Item', 'description': 'Updated Description', 'price': 20.0,'menu_item_pk': self.menu_item.pk}
        self.client.force_authenticate(user=self.user, token= self.token)
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.name, data['name'])
        self.assertEqual(self.menu_item.description, data['description'])
        self.assertEqual(self.menu_item.price, data['price'])

    def test_delete_menu_item(self):
        response = self.client.delete(self.url, data={'menu_item_pk': self.menu_item.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MenuItem.objects.filter(pk=self.menu_item.pk).exists())

    def test_retrieve_nonexistent_menu_item(self):
        url = reverse('menu:menu-item-detail', kwargs={'pk': '541abe7f-2419-482f-941b-941e72e6a23a'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_menu_item(self):
        url = reverse('menu:menu-item-detail', kwargs={'pk': '541abe7f-2419-482f-941b-941e72e6a23a'})
        data = {'name': 'Updated Item', 'description': 'Updated Description', 'price': 20.0}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_nonexistent_menu_item(self):
        url = reverse('menu:menu-item-detail', kwargs={'pk': '541abe7f-2419-482f-941b-941e72e6a23a'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_request(self):
        data = {'name': 'Updated Item', 'description': 'Updated Description', 'price': 20.0,'menu_item_pk': self.menu_item.pk}

        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_menu_item_owned_by_another_user(self):
        data = {'name': 'Updated Item', 'description': 'Updated Description', 'price': 20.0,'menu_item_pk': self.menu_item.pk}

        another_user = User.objects.create(username="testuser2", first_name="Test", last_name="User",
                                        phone_number="1234267890", email="testuser2@example.com",
                                        is_active=True, is_admin=False, is_staff=False)
        self.menu_item.menu.owner = another_user
        self.menu_item.menu.save()
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)