from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from accounts.api.views import task_send_otp

import json


class RegisterTest(TestCase):
    """ Test module for registering a new users """

    def setUp(self):
        self.client = Client()
        self.valid_payload = {
            'username': 'Muffin',
            'phone_number': '09909999999',
            'email': 'email@d.com',
            'password': 'pakdkwkwss'
        }
        self.invalid_payload = {
            'username': 'Muffin',
            'phone_number': '09909999',
            'email': 'email@d.com',
        }

    @patch.object(task_send_otp, 'delay')
    def test_failed_sms(self, mocked_send_otp):
        mocked_send_otp.return_value = False
        response = self.client.post(
            reverse('api:register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    @patch.object(task_send_otp, 'delay')
    def test_successful_sms(self, mocked_send_otp):
        mocked_send_otp.return_value = True
        response = self.client.post(
            reverse('api:register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)