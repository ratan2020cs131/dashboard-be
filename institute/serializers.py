from rest_framework import serializers
from .models import Institute

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'
    
    def to_internal_value(self, data):
        required_fields = [field.name for field in Institute._meta.fields if not field.null and not field.blank]
        
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError({"message": "Insufficient data"})
        
        return super().to_internal_value(data)