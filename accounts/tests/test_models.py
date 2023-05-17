from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTest(TestCase):
    """ Test module for User model """

    def test_create_user(self):
        user = get_user_model().objects.create(username="moel",phone_number='09909900999'\
            ,email="normal@user.com",password="passwordsimple")
        self.assertEqual(user.email, 'normal@user.com')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="moel", phone_number="123456789", email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)