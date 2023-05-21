from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import serializers
from ..serializers import UserSerializer

User = get_user_model()

class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@test.com',
            'password': 'testpassword123',
            'username': 'testuser',
            'phone_number': '09905150258',
            'first_name': 'Test',
            'last_name': 'User',
            'profile_image': None
        }
        self.serializer = UserSerializer(data=self.user_data)

    def test_serializer_with_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serializer_with_blank_username(self):
        self.user_data['username'] = ''
        self.serializer = UserSerializer(data=self.user_data)
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(self.serializer.errors['username'][0], 'Username cannot be blank.')

    def test_serializer_with_blank_password(self):
        self.user_data['password'] = ''
        self.serializer = UserSerializer(data=self.user_data)
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(self.serializer.errors['password'][0], 'Password cannot be blank.')

    def test_serializer_with_blank_phone_number(self):
        self.user_data['phone_number'] = ''
        self.serializer = UserSerializer(data=self.user_data)
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(self.serializer.errors['phone_number'][0], 'Phonenumber cannot be blank.')

    def test_serializer_with_existing_username(self):
        user = User.objects.create_user(**self.user_data)
        self.user_data['email'] = 'newemail@test.com'
        self.serializer = UserSerializer(data=self.user_data)
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(self.serializer.errors['username'][0], 'This username has already been taken. Please choose a different one.')

    def test_serializer_with_existing_phone_number(self):
        user = User.objects.create_user(**self.user_data)
        self.user_data['email'] = 'newemail@test.com'
        self.user_data['username'] = 'newusername'
        self.serializer = UserSerializer(data=self.user_data)
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(self.serializer.errors['phone_number'][0], 'This phone number has already been taken. Please choose a different one.')

    def test_serializer_with_short_password(self):
        self.user_data['password'] = '1234567'
        self.serializer = UserSerializer(data=self.user_data)
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(self.serializer.errors['non_field_errors'][0], 'Password must be at least 8 characters.')