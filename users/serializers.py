from rest_framework import serializers
from .models import User

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
