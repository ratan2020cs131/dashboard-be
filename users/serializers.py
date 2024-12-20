from rest_framework import serializers
from .models import User
from constants.roles import Roles

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SigninSerializer(serializers.Serializer):
    email = serializers.CharField()

    def to_internal_value(self, data):
        if 'email' not in data:
            raise serializers.ValidationError({"message": "Email is missing"})
        return super().to_internal_value(data)


class VerifyUserSerializer(serializers.Serializer):
    session_token = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)

    def to_internal_value(self, data):
        missing_fields = []
        if 'session_token' not in data:
            missing_fields.append('session token')
        if 'otp' not in data:
            missing_fields.append('otp')

        if missing_fields:
            missing_fields_str = ' and '.join(missing_fields)
            raise serializers.ValidationError({"message": f"{missing_fields_str} missing"})
        return super().to_internal_value(data)


class UpdateRoleSerializer(serializers.Serializer):
    role = serializers.CharField(required=True)

    def to_internal_value(self, data):
        if 'role' not in data:
            raise serializers.ValidationError({"message": "role is missing"})
        try:
            Roles(data['role'])
        except ValueError:
            valid_roles = [role.value for role in Roles]
            raise serializers.ValidationError({"message": f"Invalid role. Must be one of: {', '.join(valid_roles)}"})
        return super().to_internal_value(data)
