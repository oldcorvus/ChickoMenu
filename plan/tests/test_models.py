from django.test import TestCase
from plan.models import Plan, PlanItem, UserPlan
from django.contrib.auth import get_user_model

User = get_user_model()

class PlanModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.plan_item1 = PlanItem.objects.create(
            name='Item 1',
            description='This is item 1'
        )
        cls.plan_item2 = PlanItem.objects.create(
            name='Item 2',
            description='This is item 2'
        )
        cls.plan = Plan.objects.create(
            name='Basic Plan',
            description='This is a basic plan',
            price=10.0
        )
        cls.plan.features.add(cls.plan_item1)
        cls.plan.features.add(cls.plan_item2)

    def test_plan_name(self):
        plan = Plan.objects.get(id=self.plan.id)
        self.assertEqual(plan.name, 'Basic Plan')

    def test_plan_description(self):
        plan = Plan.objects.get(id=self.plan.id)
        self.assertEqual(plan.description, 'This is a basic plan')

    def test_plan_price(self):
        plan = Plan.objects.get(id=self.plan.id)
        self.assertEqual(plan.price, 10.0)

    def test_plan_str(self):
        plan = Plan.objects.get(id=self.plan.id)
        self.assertEqual(str(plan), 'Basic Plan')

    def test_plan_items(self):
        plan = Plan.objects.get(id=self.plan.id)
        self.assertEqual(list(plan.features.all()), [self.plan_item1, self.plan_item2])

    def test_plan_item_name(self):
        plan_item = PlanItem.objects.get(id=self.plan_item1.id)
        self.assertEqual(plan_item.name, 'Item 1')

    def test_plan_item_description(self):
        plan_item = PlanItem.objects.get(id=self.plan_item1.id)
        self.assertEqual(plan_item.description, 'This is item 1')

    def test_plan_item_str(self):
        plan_item = PlanItem.objects.get(id=self.plan_item1.id)
        self.assertEqual(str(self.plan_item1), 'Item 1')


class PlanItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.plan_item = PlanItem.objects.create(
            name='Item 1',
            description='This is item 1'
        )

    def test_plan_item_name(self):
        plan_item = PlanItem.objects.get(id=self.plan_item.id)
        self.assertEqual(plan_item.name, 'Item 1')

    def test_plan_item_description(self):
        plan_item = PlanItem.objects.get(id=self.plan_item.id)
        self.assertEqual(plan_item.description, 'This is item 1')

    def test_plan_item_str(self):
        plan_item = PlanItem.objects.get(id=self.plan_item.id)
        self.assertEqual(str(plan_item), 'Item 1')





class UserPlanTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)

        self.plan = Plan.objects.create(name='Basic', price=10.00)
        self.plan2 = Plan.objects.create(name='Pro', price=100.00)

    def test_user_plan_creation(self):
        user_plan = UserPlan.objects.create(user=self.user, plan=self.plan)
        self.assertIsInstance(user_plan, UserPlan)
        self.assertEqual(user_plan.user, self.user)
        self.assertEqual(user_plan.plan, self.plan)

    def test_user_plan_activation(self):
        user_plan = UserPlan.objects.create(user=self.user, plan=self.plan)
        user_plan.activate()
        self.assertTrue(user_plan.is_active)
        self.assertIsNone(user_plan.end_date)

    def test_user_plan_deactivation(self):
        user_plan = UserPlan.objects.create(user=self.user, plan=self.plan)
        user_plan.activate()
        user_plan.deactivate()
        self.assertFalse(user_plan.is_active)
        self.assertIsNotNone(user_plan.end_date)

    def test_user_plan_activate_with_active_plan(self):
        user_plan1 = UserPlan.objects.create(user=self.user, plan=self.plan)
        user_plan2 = UserPlan.objects.create(user=self.user, plan=self.plan2)
        user_plan1.activate()
        user_plan2.activate()
        user_plan1.refresh_from_db()
        user_plan2.refresh_from_db()

        self.assertFalse(user_plan1.is_active)
        self.assertTrue(user_plan2.is_active)

    def test_user_plan_unique_together(self):
        UserPlan.objects.create(user=self.user, plan=self.plan)
        with self.assertRaises(Exception):
            UserPlan.objects.create(user=self.user, plan=self.plan)