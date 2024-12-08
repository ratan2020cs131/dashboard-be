from rest_framework import serializers
from .models import Institute
from users.serializers import UserSerializer

class InstituteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    institute_code = serializers.CharField(
        validators=[]
    )
    
    class Meta:
        model = Institute
        fields = ['id', 'institute_code', 'institute_name', 'institute_city', 'user']
    
    def to_internal_value(self, data):
        required_fields = [field.name for field in Institute._meta.fields if not field.null and not field.blank]
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError({"message": "Insufficient data"})
        institute_code = data.get('institute_code')
        if Institute.objects.filter(institute_code=institute_code).exists():
            raise serializers.ValidationError({"message": "institute with this institute code already exists"})
        return super().to_internal_value(data)