from django.test import TestCase
from django.contrib.auth import get_user_model
import json
from unittest import mock
from django.test import TestCase, Client
from django.urls import reverse
from utils.otp import otp_generator
from django.core.cache import cache
client = Client()


class RegisterTest(TestCase):
    """ Test module for registering a new users """
    
    @classmethod
    def setUpTestData(cls):
        cache.clear()

    def setUp(self):
        self.valid_payload = {
            'username': 'Muffin',
            'phone_number': '09909999999',
            'email': 'email@d.com',
            'password': 'paswkkwks'
        }
        self.invalid_payload = {
            'username': 'Muffin',
            'phone_number': '09909999',
            'email': 'email@d.com',
        }

    @mock.patch('accounts.api.views.task_send_otp.delay')
    def test_inactive_without_verify(self, mocked_send_otp):
        mocked_send_otp.return_value = True

        response = client.post(
            reverse('api:register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        user = get_user_model().objects.get(username=self.valid_payload['username'],
                                            phone_number=self.valid_payload['phone_number'])
        self.assertFalse(user.is_active)

    @mock.patch('accounts.api.views.task_send_otp.delay')
    @mock.patch('accounts.api.views.otp_generator')
    def test_active_with_verify(self, mocked_otp, mocked_send_otp):
        mocked_otp.return_value = '131381'
        mocked_send_otp.return_value = True
        response = client.post(
            reverse('api:register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        user = get_user_model().objects.get(username=self.valid_payload['username'],
                                            phone_number=self.valid_payload['phone_number'])
        self.assertFalse(user.is_active)

        verify_response = client.post(
            reverse('api:verify-otp'),
            data=json.dumps({'code': '131381'}),
            content_type='application/json'
        )
        user = get_user_model().objects.get(username=self.valid_payload['username'],
                                            phone_number=self.valid_payload['phone_number'])
        self.assertTrue(user.is_active)

    def test_throttle(self):
        # throttle 8 per hour
        for _ in range(9):
            response = client.post(
                reverse('api:verify-otp'),
                data=json.dumps({'code': '131381'}),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 429)