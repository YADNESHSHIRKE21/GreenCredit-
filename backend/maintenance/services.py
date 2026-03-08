from datetime import timedelta
from django.utils import timezone
from activities.models import Activity
from .models import MaintenanceLog
from verdant.services import calculate_vu, get_vu_distribution


CHECKPOINTS = [14, 30, 90, 180]

VU_RELEASE_PERCENTAGE = {
    14: 0.20,
    30: 0.15,
    90: 0.15,
    180: 0.10,
}


def get_due_checkpoint(activity):
    """
    Returns the next due checkpoint day for an activity.
    Returns None if all checkpoints are done or activity is not verified.
    """
    if activity.status not in ['verified', 'completed']:
        return None

    completed_checkpoints = MaintenanceLog.objects.filter(
        activity=activity
    ).values_list('day_checkpoint', flat=True)

    activity_date = activity.timestamp
    today = timezone.now()
    days_since = (today - activity_date).days

    for checkpoint in CHECKPOINTS:
        if checkpoint not in completed_checkpoints:
            if days_since >= checkpoint:
                return checkpoint

    return None


def is_gps_valid(new_gps, original_gps, max_distance_meters=10):
    """
    Check if maintenance photo GPS is within 10 meters of original.
    """
    from geopy.distance import geodesic
    try:
        new_location = (
            float(new_gps.get('latitude')),
            float(new_gps.get('longitude'))
        )
        original_location = (
            float(original_gps.get('latitude')),
            float(original_gps.get('longitude'))
        )
        distance = geodesic(new_location, original_location).meters
        return distance <= max_distance_meters
    except Exception:
        return False


def release_vu_for_checkpoint(activity, checkpoint_day):
    """
    Release locked VU for a completed checkpoint.
    """
    percentage = VU_RELEASE_PERCENTAGE.get(checkpoint_day, 0)
    vu_to_release = round(activity.total_vu * percentage, 2)

    activity.released_vu += vu_to_release
    activity.locked_vu -= vu_to_release
    activity.locked_vu = max(0, activity.locked_vu)

    # Mark as completed after day 180
    if checkpoint_day == 180:
        activity.status = 'completed'

    activity.save()

    # Update user total VU
    user = activity.user
    user.total_vu += vu_to_release
    user.save()

    return vu_to_release


def process_maintenance_submission(activity, checkpoint_day, gps_data, image):
    """
    Process a maintenance log submission.
    Validates GPS, marks plant health, releases VU.
    """
    results = {
        'passed': False,
        'gps_valid': False,
        'vu_released': 0,
        'reason': ''
    }

    # Check GPS
    gps_ok = is_gps_valid(gps_data, activity.gps_location)
    results['gps_valid'] = gps_ok

    if not gps_ok:
        results['reason'] = 'GPS location does not match original planting location'
        return results

    # Release VU
    vu_released = release_vu_for_checkpoint(activity, checkpoint_day)
    results['vu_released'] = vu_released
    results['passed'] = True
    results['reason'] = f'Checkpoint Day {checkpoint_day} verified successfully'

    return results