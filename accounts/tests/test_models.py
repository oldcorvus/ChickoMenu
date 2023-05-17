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

