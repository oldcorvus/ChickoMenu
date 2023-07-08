from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from theme.models import Theme
from django.contrib.auth import get_user_model
from utils.test_tools import temporary_image

User = get_user_model()

class ThemeListCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass',
        email="testemail@email.com", phone_number="09905150258")
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)
        self.theme = Theme.objects.create(name='Test Theme')

    def test_list_themes(self):
        url = reverse('theme:theme-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Theme.objects.count())

    def test_create_theme(self):
        url = reverse('theme:theme-list')
        data = {
            'name':'Test',
            'font_family':'Times New Roman',
            'menu_background_color':'#ffffff',
            'menu_text_color':'#000000',
            'logo_image': temporary_image(),
            'header_color': '#ffffff',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Theme.objects.count(), 2)

class ThemeRetrieveUpdateDestroyAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass',
        email="testemail@email.com", phone_number="09905150258")
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)
        self.theme = Theme.objects.create(name='Test Theme')

    def test_retrieve_theme(self):
        url = reverse('theme:theme-detail', kwargs={'pk': self.theme.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Theme')

    def test_update_theme(self):
        url = reverse('theme:theme-detail', kwargs={'pk': self.theme.pk})
        data = {
            'name': 'Updated Theme',
            'logo_image': temporary_image(),
            'header_color': '#343a40',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.theme.refresh_from_db()
        self.assertEqual(self.theme.name, 'Updated Theme')

    def test_delete_theme(self):
        url = reverse('theme:theme-detail', kwargs={'pk': self.theme.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Theme.objects.filter(pk=self.theme.pk).exists())