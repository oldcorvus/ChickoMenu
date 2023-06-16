from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


def check_phone_number(value):
    if len(value) > 11 or len(value) < 11:
        raise serializers.ValidationError(_('phone number is not valid'))
    if not value.startswith('09'):
        raise serializers.ValidationError(_('phone number should start with 09'))

    return value