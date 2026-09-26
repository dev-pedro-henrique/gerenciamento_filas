from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import User
from .services import terminate_user_session


class CurrentUserSerializer(serializers.ModelSerializer):
    role_label = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "name", "role", "role_label")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, trim_whitespace=True)
    password = serializers.CharField(trim_whitespace=False, write_only=True)


class ReceptionistSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ("id", "username", "name", "password", "is_active", "date_joined")
        read_only_fields = ("id", "date_joined")

    def validate_username(self, value: str) -> str:
        return value.strip().lower()

    def validate_password(self, value: str) -> str:
        try:
            password_validation.validate_password(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(list(error.messages)) from error
        return value

    def create(self, validated_data):
        return User.objects.create_user(role=User.Role.RECEPTIONIST, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        was_active = instance.is_active
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        if password:
            instance.set_password(password)
        instance.full_clean()
        instance.save()
        if (was_active and not instance.is_active) or password:
            terminate_user_session(instance)
        return instance


class ReceptionistUpdateSerializer(ReceptionistSerializer):
    password = serializers.CharField(write_only=True, required=False, trim_whitespace=False)


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate_password(self, value: str) -> str:
        try:
            password_validation.validate_password(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(list(error.messages)) from error
        return value
