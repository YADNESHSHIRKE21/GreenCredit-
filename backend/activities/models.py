from django.db import models
from users.models import User

class Activity(models.Model):
    SOIL_CHOICES = [
        ('none', 'No Preparation'),
        ('basic', 'Basic'),
        ('enriched', 'Enriched'),
        ('professional', 'Professional'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    plant_species = models.CharField(max_length=100)
    plant_count = models.IntegerField()
    soil_preparation = models.CharField(max_length=20, choices=SOIL_CHOICES)
    time_spent = models.FloatField(help_text="Time in hours")
    gps_location = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    initial_image = models.ImageField(upload_to='activities/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_vu = models.FloatField(default=0)
    released_vu = models.FloatField(default=0)
    locked_vu = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.plant_species} ({self.timestamp.date()})"