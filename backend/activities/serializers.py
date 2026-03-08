from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            'id',
            'plant_species',
            'plant_count',
            'soil_preparation',
            'time_spent',
            'gps_location',
            'timestamp',
            'initial_image',
            'status',
            'total_vu',
            'released_vu',
            'locked_vu',
        ]
        read_only_fields = ['timestamp', 'status', 'total_vu', 'released_vu', 'locked_vu']