from django.db import models
from users.models import User
from activities.models import Activity

class Recognition(models.Model):
    BADGE_CHOICES = [
        ('1_year_survivor', '🌱 1-Year Survivor'),
        ('tree_guardian', '🌳 Tree Guardian'),
        ('urban_forest_keeper', '🌲 Urban Forest Keeper'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recognitions')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='recognitions')
    badge_type = models.CharField(max_length=30, choices=BADGE_CHOICES)
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.badge_type}"