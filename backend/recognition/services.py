from django.utils import timezone
from datetime import timedelta
from activities.models import Activity
from .models import Recognition


BADGE_THRESHOLDS = {
    '1_year_survivor': 365,
    'tree_guardian': 730,
    'urban_forest_keeper': 1095,
}


def check_and_award_badges(user):
    """
    Check all completed activities and award badges based on survival time.
    """
    awarded = []
    completed_activities = Activity.objects.filter(
        user=user,
        status='completed'
    )

    for activity in completed_activities:
        days_alive = (timezone.now() - activity.timestamp).days

        for badge_type, threshold_days in BADGE_THRESHOLDS.items():
            if days_alive >= threshold_days:
                already_awarded = Recognition.objects.filter(
                    user=user,
                    activity=activity,
                    badge_type=badge_type
                ).exists()

                if not already_awarded:
                    Recognition.objects.create(
                        user=user,
                        activity=activity,
                        badge_type=badge_type
                    )
                    awarded.append({
                        'badge': badge_type,
                        'activity_id': activity.id,
                        'plant_species': activity.plant_species,
                    })

    return awarded


def update_urban_forest_score(user):
    """
    Urban Forest Score = number of trees survived 1 year.
    """
    one_year_ago = timezone.now() - timedelta(days=365)
    survived = Activity.objects.filter(
        user=user,
        status='completed',
        timestamp__lte=one_year_ago
    ).count()

    user.trees_survived_one_year = survived
    user.urban_forest_score = survived
    user.save()

    return survived


def get_leaderboard():
    """
    Returns top 10 users ranked by urban forest score.
    """
    from users.models import User
    top_users = User.objects.order_by('-urban_forest_score')[:10]

    leaderboard = []
    for rank, user in enumerate(top_users, start=1):
        leaderboard.append({
            'rank': rank,
            'username': user.username,
            'urban_forest_score': user.urban_forest_score,
            'trees_planted': user.trees_planted,
            'trees_survived_one_year': user.trees_survived_one_year,
            'total_vu': user.total_vu,
        })

    return leaderboard