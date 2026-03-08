from rest_framework import serializers
from .models import MaintenanceLog

class MaintenanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceLog
        fields = [
            'id',
            'activity',
            'day_checkpoint',
            'image',
            'gps_location',
            'timestamp',
            'plant_health',
            'vu_released',
        ]
        read_only_fields = ['timestamp', 'plant_health', 'vu_released']