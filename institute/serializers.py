from rest_framework import serializers
from .models import Institute
from users.serializers import UserSerializer

class InstituteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    institute_code = serializers.CharField(validators=[])
    
    class Meta:
        model = Institute
        fields = ['id', 'institute_code', 'institute_name', 'institute_city', 'user']
    
    def to_internal_value(self, data):
        # Check for missing fields
        required_fields = [field.name for field in Institute._meta.fields if not field.null and not field.blank]
        missing_fields = [field for field in required_fields if field not in data or not data.get(field)]
        if missing_fields:
            raise serializers.ValidationError({"message": "Insufficient data"})
        
        # Check for unique institute code
        institute_code = data.get('institute_code')
        if Institute.objects.filter(institute_code=institute_code).exists():
            raise serializers.ValidationError({"message": "Institute with this institute code already exists"})
        
        return super().to_internal_value(data)
    
    def validate(self, data):
        # Override to handle blank fields
        for field in ['institute_name', 'institute_city', 'institute_code']:
            if not data.get(field):
                raise serializers.ValidationError({"message": "Insufficient data"})
        return data
