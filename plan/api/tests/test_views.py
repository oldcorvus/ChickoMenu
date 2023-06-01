from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from plan.models import Plan, PlanItem
from plan.api.serializers import PlanSerializer, PlanItemSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class PlanViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.plan1 = Plan.objects.create(
            name='Basic',
            description='This is a basic plan',
            price=10.00
        )
        self.plan2 = Plan.objects.create(
            name='Premium',
            description='This is a premium plan',
            price=20.00
        )
        self.plan_item_1 = PlanItem.objects.create(
            name='Feature 1',
            description='This is feature 1'
        )
        self.plan_item_2 = PlanItem.objects.create(
            name='Feature 2',
            description='This is feature 2'
        )
        self.plan1.features.add(self.plan_item_1, self.plan_item_2)
        self.plan2.features.add(self.plan_item_1)

    def test_plan_list(self):
        url = reverse('plan:plan-list')
        response = self.client.get(url)
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_plan_detail(self):
        url = reverse('plan:plan-detail', args=[self.plan1.id])
        response = self.client.get(url)
        plan = Plan.objects.get(id=self.plan1.id)
        serializer = PlanSerializer(plan)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_plan_create(self):
        url = reverse('plan:plan-list')
        data = {
            'name': 'Pro',
            'description': 'This is a pro plan',
            'price': 30.00,
            'features':  [{'name': 'Feature 1', 'description': 'This is feature 1'}]
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Plan.objects.count(), 3)
        self.assertEqual(Plan.objects.get(name='Pro').name, 'Pro')

    def test_plan_update(self):
        url = reverse('plan:plan-detail', args=[self.plan1.id])
        data = {
            'name': 'Basic Plus',
            'description':'This is a basic plus plan',
            'price' : 15.00,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Plan.objects.get(id=self.plan1.id).name, 'Basic Plus')
        self.assertEqual(Plan.objects.get(id=self.plan1.id).description, 'This is a basic plus plan')
        self.assertEqual(Plan.objects.get(id=self.plan1.id).price, 15.00)
        self.assertEqual(Plan.objects.get(id=self.plan1.id).features.count(), 2)
        self.assertIn(self.plan_item_2, Plan.objects.get(id=self.plan1.id).features.all()) 

    def test_plan_delete(self):
        url = reverse('plan:plan-detail', args=[self.plan1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Plan.objects.count(), 1)

    def test_plan_permission_classes(self):
        self.client.credentials()
        url = reverse('plan:plan-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)