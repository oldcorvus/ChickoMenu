from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from plan.models import Plan, PlanItem, UserPlan
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

class PlanItemViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.plan_item1 = PlanItem.objects.create(
        name='Feature 1',
        description='This is feature 1'
        )
        self.plan_item2 = PlanItem.objects.create(
        name='Feature 2',
        description='This is feature 2'
        )


    def test_plan_item_list(self):
        url = reverse('plan:planitem-list')
        response = self.client.get(url)
        plan_items = PlanItem.objects.all()
        serializer = PlanItemSerializer(plan_items, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_plan_item_detail(self):
        url = reverse('plan:planitem-detail', args=[self.plan_item1.id])
        response = self.client.get(url)
        plan_item = PlanItem.objects.get(id=self.plan_item1.id)
        serializer = PlanItemSerializer(plan_item)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_plan_item_create(self):
        url = reverse('plan:planitem-list')
        data = {
            'name': 'Feature 3',
            'description': 'This is feature 3'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlanItem.objects.count(), 3)
        self.assertEqual(PlanItem.objects.get(name='Feature 3').name, 'Feature 3')

    def test_plan_item_update(self):
        url = reverse('plan:planitem-detail', args=[self.plan_item1.id])
        data = {
            'name': 'Feature 1 Plus',
            'description': 'This is feature 1 plus'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PlanItem.objects.get(id=self.plan_item1.id).name, 'Feature 1 Plus')
        self.assertEqual(PlanItem.objects.get(id=self.plan_item1.id).description, 'This is feature 1 plus')

    def test_plan_item_delete(self):
            url = reverse('plan:planitem-detail', args=[self.plan_item1.id])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertFalse(PlanItem.objects.filter(id=self.plan_item1.id).exists())
            self.assertTrue(PlanItem.objects.filter(id=self.plan_item2.id).exists())


class UserPlanCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser2", first_name="Test", last_name="User",
                                        phone_number="1234567891", email="tes2tuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)
        self.plan1 = Plan.objects.create(
            name='Basic',
            description='This is a basic plan',
            price=10.00
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user, token= self.token)

    def test_create_user_plan(self):
        url = reverse('plan:user_plan_create')
        data = {'plan': self.plan1.id,   
                 'user' : self.user.id}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserPlan.objects.count(), 1)
        self.assertEqual(UserPlan.objects.get().user, self.user)
        self.assertEqual(UserPlan.objects.get().plan, self.plan1)


class UserPlansAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
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
        self.user_plan1 = UserPlan.objects.create(user=self.user, plan= self.plan1)
        self.user_plan2 = UserPlan.objects.create(user=self.user, plan= self.plan2)

    def test_list_user_plans(self):
        url = reverse('plan:user_plans', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.user_plan1.id)
        self.assertEqual(response.data[0]['plan'], self.user_plan1.plan.id)
        self.assertEqual(response.data[1]['id'], self.user_plan2.id)
        self.assertEqual(response.data[1]['plan'], self.user_plan2.plan.id)

    def test_list_user_plans_unauthenticated(self):
        self.client.logout()
        url = reverse('plan:user_plans', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

