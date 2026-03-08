from django.db import models
from activities.models import Activity

class MaintenanceLog(models.Model):
    CHECKPOINT_CHOICES = [
        (14, 'Day 14'),
        (30, 'Day 30'),
        (90, 'Day 90'),
        (180, 'Day 180'),
    ]

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='maintenance_logs')
    day_checkpoint = models.IntegerField(choices=CHECKPOINT_CHOICES)
    image = models.ImageField(upload_to='maintenance/')
    gps_location = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    plant_health = models.BooleanField(default=False)
    vu_released = models.FloatField(default=0)

    def __str__(self):
        return f"Activity {self.activity.id} - Day {self.day_checkpoint}"