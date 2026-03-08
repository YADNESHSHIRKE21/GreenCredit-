from rest_framework import serializers
from .models import Recognition


class RecognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recognition
        fields = [
            'id',
            'badge_type',
            'date_awarded',
            'activity',
        ]