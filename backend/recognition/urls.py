from django.urls import path
from .views import CheckBadgesView, UserBadgesView, LeaderboardView

urlpatterns = [
    path('check/', CheckBadgesView.as_view(), name='check-badges'),
    path('badges/', UserBadgesView.as_view(), name='user-badges'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]