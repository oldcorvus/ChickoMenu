from django.test import TestCase
from ..models import User, SMSVerification

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", first_name="Test", last_name="User",
                                        phone_number="1234567890", email="testuser@example.com",
                                        is_active=True, is_admin=False, is_staff=False)

    def test_user_creation(self):
        user = User.objects.get(username="testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.phone_number, "1234567890")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)

    def test_str_representation(self):
        user = User.objects.get(username="testuser")
        self.assertEqual(str(user), "testuser--1234567890")



class SMSVerificationTestCase(TestCase):
    def setUp(self):
        self.sms_data = {
            'security_code': '1234',
            'phone_number': '+1234567890',
            'session_token': 'abc123',
            'is_verified': False
        }
        self.sms_verification = SMSVerification.objects.create(**self.sms_data)

    def test_sms_verification_creation(self):
        self.assertTrue(isinstance(self.sms_verification, SMSVerification))
        self.assertEqual(str(self.sms_verification), f"{self.sms_verification.phone_number}: {self.sms_verification.security_code}")
        self.assertEqual(SMSVerification.objects.count(), 1)

    def test_sms_verification_fields(self):
        self.assertEqual(self.sms_verification.security_code, '1234')
        self.assertEqual(str(self.sms_verification.phone_number), '+1234567890')
        self.assertEqual(self.sms_verification.session_token, 'abc123')
        self.assertFalse(self.sms_verification.is_verified)

