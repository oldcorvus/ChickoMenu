from django.test import TestCase
from plan.models import UserPlan
from ..models import Order
from plan.models import Plan, UserPlan
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)

        plan = Plan.objects.create(name='Basic', price=10.00)
        # Create a UserPlan object
        cls.user_plan =  UserPlan.objects.create(plan= plan, user= user)
        # Create an Order object
        cls.order = Order.objects.create(
            user_plan= cls.user_plan,
            payable_amount=10.00,
            is_paid=True,
            authority='1234567890'
        )

    def test_order_fields(self):
        order = Order.objects.get(id=self.order.id)
        expected_user_plan = self.user_plan
        self.assertEqual(order.user_plan, expected_user_plan)
        self.assertEqual(order.payable_amount, 10.00)
        self.assertTrue(order.is_paid)
        self.assertEqual(order.authority, '1234567890')

    def test_order_defaults(self):
        order = Order.objects.create(user_plan=self.user_plan)
        self.assertEqual(order.payable_amount, 0.00)
        self.assertFalse(order.is_paid)
        self.assertIsNone(order.authority)