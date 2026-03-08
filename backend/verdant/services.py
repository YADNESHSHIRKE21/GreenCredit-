def get_impact_potential(plant_species):
    """
    Returns impact score based on plant species type.
    """
    species_map = {
        'herb': 2,
        'shrub': 3,
        'fruit tree': 5,
        'native tree': 6,
        'large canopy tree': 8,
    }

    plant_lower = plant_species.lower()
    for key, value in species_map.items():
        if key in plant_lower:
            return value

    return 3  # default score for unknown species


def get_effort_score(plant_count, soil_preparation, time_spent):
    """
    Returns effort score based on planting effort.
    """
    score = 0

    # Score from plant count
    if plant_count >= 20:
        score += 3
    elif plant_count >= 10:
        score += 2
    elif plant_count >= 5:
        score += 1

    # Score from soil preparation
    soil_scores = {
        'none': 0,
        'basic': 1,
        'enriched': 2,
        'professional': 3,
    }
    score += soil_scores.get(soil_preparation, 0)

    # Score from time spent
    if time_spent >= 8:
        score += 3
    elif time_spent >= 4:
        score += 2
    elif time_spent >= 1:
        score += 1

    # Normalize to 1-5 scale
    if score >= 8:
        return 5
    elif score >= 6:
        return 4
    elif score >= 4:
        return 3
    elif score >= 2:
        return 2
    else:
        return 1


def get_sustainability_multiplier(maintenance_logs_count):
    """
    Multiplier increases as maintenance checkpoints are completed.
    Starts at 1.0, increases with each verified checkpoint.
    """
    multipliers = {
        0: 1.0,
        1: 1.2,
        2: 1.5,
        3: 1.8,
        4: 2.0,
    }
    return multipliers.get(maintenance_logs_count, 2.0)


def calculate_vu(activity, maintenance_logs_count=0):
    """
    Main VU calculation function.
    VU = (Impact Potential x Effort Invested) x Sustainability Multiplier
    """
    impact = get_impact_potential(activity.plant_species)
    effort = get_effort_score(
        activity.plant_count,
        activity.soil_preparation,
        activity.time_spent
    )
    multiplier = get_sustainability_multiplier(maintenance_logs_count)

    total_vu = (impact * effort) * multiplier
    return round(total_vu, 2)


def get_vu_distribution(total_vu):
    """
    Splits total VU into initial release and locked amounts.
    Initial release = 40% of total VU
    Remaining 60% is locked for maintenance verification
    """
    initial_release = round(total_vu * 0.4, 2)
    locked = round(total_vu * 0.6, 2)

    return {
        'total_vu': total_vu,
        'initial_release': initial_release,
        'locked_vu': locked,
        'checkpoint_distribution': {
            'day_14': round(total_vu * 0.2, 2),
            'day_30': round(total_vu * 0.15, 2),
            'day_90': round(total_vu * 0.15, 2),
            'day_180': round(total_vu * 0.10, 2),
        }
    }