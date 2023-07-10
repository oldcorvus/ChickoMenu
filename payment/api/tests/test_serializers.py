from django.test import TestCase
from decimal import Decimal
from payment.models import Order
from plan.models import Plan, UserPlan
from ..serializers import OrderSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass',
        email="testemail@email.com", phone_number="09905150258")

        self.plan = Plan.objects.create(
            name='Premium Plan',
            price=Decimal('9.99'),
        )
        self.user_plan = UserPlan.objects.create(
            user=self.user,
            plan=self.plan,
            is_active=True
            
        )
        self.order = Order.objects.create(
            user_plan=self.user_plan,
            payable_amount=self.plan.price,
            is_paid=True,
            authority='12345'
        )
        self.serializer_data = {
            'payable_amount': str(self.plan.price),
            'is_paid': False,
            'authority': '67890'
        }
        self.serializer = OrderSerializer(instance=self.order)

    def test_serializer_contains_expected_fields(self):
        expected_fields = {'id', 'user_plan', 'payable_amount', 'is_paid', 'authority'}
        self.assertEqual(set(self.serializer.data.keys()), expected_fields)

    def test_serializer_data(self):
        self.assertEqual(str(self.serializer.data['id']), str(self.order.id))
        self.assertEqual(self.serializer.data['payable_amount'], str(self.order.payable_amount))
        self.assertEqual(self.serializer.data['is_paid'], self.order.is_paid)
        self.assertEqual(self.serializer.data['authority'], self.order.authority)

    def test_create_valid_order(self):
        serializer = OrderSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

        order = serializer.save(user_plan=self.user_plan)

        self.assertEqual(order.user_plan, self.user_plan)
        self.assertEqual(order.payable_amount, self.plan.price)
        self.assertFalse(order.is_paid)
        self.assertEqual(order.authority, '67890')

    def test_create_invalid_order(self):
        self.serializer_data['payable_amount'] = 'invalid'
        serializer = OrderSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())

