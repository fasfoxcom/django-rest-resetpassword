from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

__all__ = [
    "EmailSerializer",
    "PasswordTokenSerializer",
    "TokenSerializer",
]


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)

    def validate(self, data):
        """
        Check email and username can't be provided together.
        """
        if not (bool(data.get("username")) ^ bool(data.get("email"))):
            raise serializers.ValidationError("Invalid Inputs, only one field required.")
        return data


class PasswordTokenSerializer(serializers.Serializer):
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}
    )
    token = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
