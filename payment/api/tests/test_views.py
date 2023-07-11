from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from payment.models import Order
from plan.models import UserPlan, Plan
from django.contrib.auth.models import User
import uuid
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class OrderListCreateAPIViewTests(APITestCase):
    def setUp(self):
        self.user =  User.objects.create_user(username='testuser', password='testpass',
        email="testemail@email.com", phone_number="09905150258")
        self.user_plan = UserPlan.objects.create(user=self.user, plan=Plan.objects.create(name='Test Plan', price=10), is_active=False)
        self.url = reverse('payment:order_list_create')
        self.token = Token.objects.create(user=self.user)

    def test_create_order_with_valid_user_plan_id(self):
        self.client.force_authenticate(user=self.user, token = self.token)
        data = {'user_plan_id': self.user_plan.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().user_plan, self.user_plan)


    def test_create_order_with_valid_user_free_plan(self):
        self.client.force_authenticate(user=self.user, token = self.token)
        plan = Plan.objects.create(name='Free', price=10)
        user_plan = UserPlan.objects.create(user=self.user, plan=plan)
        data = {'user_plan_id': user_plan.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get(user_plan = user_plan)
        self.assertTrue(order.user_plan.is_active)
        self.assertTrue(order.is_paid)

    def test_create_order_with_invalid_user_plan_id(self):
        self.client.force_authenticate(user=self.user, token = self.token)
        data = {'user_plan_id': uuid.uuid4()} 
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_without_authentication(self):
        data = {'user_plan_id': self.user_plan.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Order.objects.count(), 0)

class OrderDetailAPIViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass',
        email="testemail@email.com", phone_number="09905150258")
        self.user_plan = UserPlan.objects.create(user=self.user, plan=Plan.objects.create(name='Test Plan', price=10), is_active=True)
        self.order = Order.objects.create(user_plan=self.user_plan, payable_amount=self.user_plan.plan.price)
        self.url = reverse('payment:order-detail', kwargs={'pk': self.order.id})
        self.token = Token.objects.create(user=self.user)

    def test_retrieve_order_detail_with_valid_user(self):
        self.client.force_authenticate(user=self.user, token = self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['id']), str(self.order.id))

    def test_retrieve_order_detail_with_invalid_user(self):
        other_user = User.objects.create_user(username='testuser2', password='testpass',
        email="testemail2s@email.com", phone_number="09905150257")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_order_detail_without_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)