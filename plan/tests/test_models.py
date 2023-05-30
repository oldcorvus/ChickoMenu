from django.test import TestCase
from plan.models import Plan, PlanItem

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
