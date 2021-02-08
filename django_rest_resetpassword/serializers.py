from django.utils.translation import ugettext_lazy as _
from django_rest_resetpassword.models import get_password_reset_lookup_fields
from django.core.validators import EmailValidator, ValidationError

from rest_framework import serializers

__all__ = [
    "EmailSerializer",
    "PasswordTokenSerializer",
    "TokenSerializer",
]


class EmailSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()

    def validate_email_or_username(self, value):
        print(get_password_reset_lookup_fields)
        if get_password_reset_lookup_fields() == ["email"]:
            try:
                validator = EmailValidator()
                validator(value)
            except ValidationError as ve:
                raise ve
        return value


class PasswordTokenSerializer(serializers.Serializer):
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}
    )
    token = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
