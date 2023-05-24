from django.test import TestCase, RequestFactory
from rest_framework.test import force_authenticate
from menu.models import Menu
from ..views import ListOfAllActiveMenus
from ..serializers import MenuSerializer
from django.contrib.auth import get_user_model


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
