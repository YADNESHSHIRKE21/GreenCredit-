import hashlib
import imagehash
from PIL import Image
from geopy.distance import geodesic
from activities.models import Activity


def compute_image_hash(image_file):
    """Generate perceptual hash of an image for duplicate detection."""
    img = Image.open(image_file)
    return str(imagehash.phash(img))


def is_duplicate_image(new_image_file, user):
    """Check if the same image was already submitted by this user."""
    new_hash = compute_image_hash(new_image_file)
    existing_activities = Activity.objects.filter(user=user)

    for activity in existing_activities:
        if activity.initial_image:
            try:
                existing_hash = compute_image_hash(activity.initial_image)
                hash1 = imagehash.hex_to_hash(new_hash)
                hash2 = imagehash.hex_to_hash(existing_hash)
                if abs(hash1 - hash2) < 10:
                    return True, activity.id
            except Exception:
                continue
    return False, None


def validate_gps_location(gps_data):
    """Validate that GPS coordinates are real and within valid range."""
    try:
        lat = float(gps_data.get('latitude'))
        lng = float(gps_data.get('longitude'))

        if not (-90 <= lat <= 90):
            return False, "Invalid latitude"
        if not (-180 <= lng <= 180):
            return False, "Invalid longitude"

        return True, "Valid location"
    except (TypeError, ValueError):
        return False, "GPS data missing or invalid"


def check_geo_cluster(gps_data, radius_meters=10):
    """Check if another activity already exists at the same location."""
    try:
        lat = float(gps_data.get('latitude'))
        lng = float(gps_data.get('longitude'))
        new_location = (lat, lng)

        existing_activities = Activity.objects.filter(status='verified')
        for activity in existing_activities:
            existing_gps = activity.gps_location
            existing_location = (
                float(existing_gps.get('latitude')),
                float(existing_gps.get('longitude'))
            )
            distance = geodesic(new_location, existing_location).meters
            if distance < radius_meters:
                return True, activity.id

        return False, None
    except Exception:
        return False, None


def verify_activity(activity, image_file=None):
    """
    Run all verification checks on a submitted activity.
    Returns a dict with results and overall pass/fail.
    """
    results = {
        'gps_valid': False,
        'duplicate_image': False,
        'geo_cluster': False,
        'passed': False,
        'reason': ''
    }

    # Check 1 - GPS Validation
    gps_valid, gps_message = validate_gps_location(activity.gps_location)
    results['gps_valid'] = gps_valid
    if not gps_valid:
        results['reason'] = gps_message
        return results

    # Check 2 - Duplicate Image Detection
    if image_file:
        is_dup, dup_id = is_duplicate_image(image_file, activity.user)
        results['duplicate_image'] = is_dup
        if is_dup:
            results['reason'] = f"Duplicate image detected (matches activity {dup_id})"
            return results

    # Check 3 - Geo Cluster Detection
    is_cluster, cluster_id = check_geo_cluster(activity.gps_location)
    results['geo_cluster'] = is_cluster
    if is_cluster:
        results['reason'] = f"Another verified activity exists at this location (activity {cluster_id})"
        results['passed'] = False
        return results

    # All checks passed
    results['passed'] = True
    results['reason'] = "All verification checks passed"
    return results