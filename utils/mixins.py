

class SetCustomErrorMessagesMixin:
    """
    Replaces built-in validator messages with messages, defined in Meta class. 
    This mixin should be inherited before the actual Serializer class in order to call __init__ method.
    """

    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super(SetCustomErrorMessagesMixin, self).__init__(*args, **kwargs)
        self.replace_validators_messages()

    def replace_validators_messages(self):
        for field_name, validators_lookup in self.custom_error_messages_for_validators.items():
            # noinspection PyUnresolvedReferences
            for validator in self.fields[field_name].validators:
                if type(validator) in validators_lookup:
                    validator.message = validators_lookup[type(validator)]

    @property
    def custom_error_messages_for_validators(self):
        meta = getattr(self, 'Meta', None)
        return getattr(meta, 'custom_error_messages_for_validators', {})