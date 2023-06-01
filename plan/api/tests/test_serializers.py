from django.test import TestCase
from plan.models import Plan, PlanItem
from ..serializers import PlanSerializer, PlanItemSerializer

class PlanSerializerTest(TestCase):
    def setUp(self):
        self.plan_item1 = PlanItem.objects.create(name='Item 1', description='This is item 1')
        self.plan_item2 = PlanItem.objects.create(name='Item 2', description='This is item 2')
        self.plan = Plan.objects.create(name='Basic Plan', description='This is a basic plan', price=10.0)
        self.plan.features.add(self.plan_item1)
        self.plan.features.add(self.plan_item2)
        self.serializer = PlanSerializer(instance=self.plan)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['name', 'description', 'price', 'features','id']))

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.plan.name)

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['description'], self.plan.description)


    def test_features_field_content(self):
        data = self.serializer.data
        self.assertEqual(len(data['features']), 2)
        self.assertEqual(data['features'][0]['name'], self.plan_item1.name)
        self.assertEqual(data['features'][0]['description'], self.plan_item1.description)
        self.assertEqual(data['features'][1]['name'], self.plan_item2.name)
        self.assertEqual(data['features'][1]['description'], self.plan_item2.description)

    def test_id_field_read_only(self):
        data = {'name': 'New Plan', 'description': 'This is a new plan', 'price': 20.0, 'id': self.id}
        serializer = PlanSerializer(instance=self.plan, data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(self.plan.name, serializer.data['name'])
        self.assertEqual(self.plan.description, serializer.data['description'])
        self.assertNotEqual(self.plan.id, data['id'])

    def test_features_field_can_be_null(self):
        data = {'name': 'New Plan', 'description': 'This is a new plan', 'price': 20.0, 'features': None}
        serializer = PlanSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(serializer.is_valid())
        plan = serializer.save()
        self.assertEqual(plan.features.count(), 0)

    def test_create_plan_with_new_plan_items(self):
        data = {'name': 'Premium Plan', 'description': 'This is a premium plan', 'price': 20.0, \
            'features': [{'name': 'Feature 1', 'description': 'This is feature 1'}, {'name': 'Feature 2', 'description': 'This is feature 2'}]}
        serializer = PlanSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        plan = serializer.save()


        self.assertEqual(plan.name, data['name'])
        self.assertEqual(plan.description, data['description'])
        self.assertEqual(plan.price, data['price'])
        self.assertEqual(plan.features.count(), 2)

        feature1 = plan.features.first()
        feature2 = plan.features.last()

        self.assertEqual(feature1.name, 'Feature 1')
        self.assertEqual(feature1.description, 'This is feature 1')
        self.assertEqual(feature2.name, 'Feature 2')
        self.assertEqual(feature2.description, 'This is feature 2')

    def test_update_plan_with_new_plan_items(self):
        data = {'name': 'Premium Plan', 'description': 'This is a premium plan', 'price': 20.0, 'features': [{'name': 'Feature 1', 'description': 'This is feature 1'}, {'name': 'Feature 2', 'description': 'This is feature 2'}]}
        serializer = PlanSerializer(instance=self.plan, data=data)
        self.assertTrue(serializer.is_valid())
        plan = serializer.save()

        self.assertEqual(plan.name, data['name'])
        self.assertEqual(plan.description, data['description'])
        self.assertEqual(plan.features.count(), 2)

        feature1 = plan.features.first()
        feature2 = plan.features.last()

        self.assertEqual(feature1.name, 'Feature 1')
        self.assertEqual(feature1.description, 'This is feature 1')
        self.assertEqual(feature2.name, 'Feature 2')
        self.assertEqual(feature2.description, 'This is feature 2')




class PlanItemSerializerTestCase(TestCase):
    def setUp(self):
        self.plan_item_data = {
            'name': 'Plan Item 1',
            'description': 'Description for Plan Item 1',
        }
        self.plan_item = PlanItem.objects.create(**self.plan_item_data)
        self.serializer = PlanItemSerializer(instance=self.plan_item)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['name', 'description'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.plan_item_data['name'])

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['description'], self.plan_item_data['description'])

    def test_id_field_read_only(self):
        data = {'name': 'New Plan', 'description': 'This is a new plan',  'id': self.id}
        serializer = PlanItemSerializer(instance=self.plan_item, data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(self.plan_item.name, serializer.data['name'])
        self.assertEqual(self.plan_item.description, serializer.data['description'])
        self.assertNotEqual(self.plan_item.id, data['id'])

    def test_create_plan_item(self):
        new_plan_item_data = {
            'name': 'Plan Item 2',
            'description': 'Description for Plan Item 2',
        }
        serializer = PlanItemSerializer(data=new_plan_item_data)
        self.assertTrue(serializer.is_valid())
        self.plan_item = serializer.save()
        plan_item = PlanItem.objects.get(id=self.plan_item.id)
        self.assertEqual(plan_item.name, new_plan_item_data['name'])
        self.assertEqual(plan_item.description, new_plan_item_data['description'])