from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    total_vu = models.FloatField(default=0)
    urban_forest_score = models.IntegerField(default=0)
    trees_planted = models.IntegerField(default=0)
    trees_survived_one_year = models.IntegerField(default=0)

    def __str__(self):
        return self.username