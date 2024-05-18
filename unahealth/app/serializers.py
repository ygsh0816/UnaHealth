from rest_framework import serializers
from .models import GlucoseLevel

class GlucoseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseLevel
        fields = ['id', 'user_id', 'timestamp', 'glucose_value', 'device_name', 'device_serial_number']
