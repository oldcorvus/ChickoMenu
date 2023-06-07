from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, BaseUniqueForValidator
from utils.mixins import SetCustomErrorMessagesMixin
from django.contrib.auth.hashers import make_password
from .validators import check_phone_number
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(SetCustomErrorMessagesMixin, serializers.ModelSerializer):
    """Serializer for the users object"""
    id = serializers.ReadOnlyField()

    class Meta:
        model = get_user_model()
        fields = ('id','email', 'password', 'username', 'phone_number',
                  'first_name', 'last_name', 'profile_image')
                  
        extra_kwargs = {
            'username': {"error_messages": {"blank": _("Username cannot be blank.")}},
            'password': {"error_messages": {"blank": _("Password cannot be blank.")}},
            'phone_number': {"error_messages": {"blank": _("Phonenumber cannot be blank.")}},
        }
        custom_error_messages_for_validators = {
            'username': {
                UniqueValidator: _('This username has already been taken. Please choose a different one.'),
                BaseUniqueForValidator: _('Username cannot be blank.'),
            },
            'phone_number': {
                UniqueValidator: _('This phone number has already been taken. Please choose a different one.'),
                BaseUniqueForValidator: _('Phone number cannot be blank.'),
            }
        }

    def validate(self, data):
        # get the password from the data
        password = data.get('password')

        # validate password
        try:
            validate_password(password=password, user=self.instance)
        except ValidationError:
            raise serializers.ValidationError(_("Password must be at least 8 characters."))

        return super().validate(data)

    def validate_phone_number(self, value):
        # validate phone number
        # use a custom phone number validation function
        return check_phone_number(value)

    def create(self, validated_data):
        # hash password
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password

        return super().create(validated_data)

class SMSVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=6,
        min_length=6,
    )

    def validate_code(self, value):
        try:
            int(value)
        except :
            raise serializers.ValidationError(_("The entered code is incorrect."))

        return value