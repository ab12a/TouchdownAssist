"""Matching logic. It only works on plain dicts, so it can be tested
without a database (requirement: matching separated from the rest)."""
from math import radians, sin, cos, asin, sqrt


def distance_km(lat1, lon1, lat2, lon2):
    """Straight-line distance between two points (haversine formula)."""
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * asin(sqrt(a))


def commute_minutes(room, university):
    """Rough estimate: 3 minutes per km plus 5 minutes for walking/waiting.
    This is NOT real route calculation (that is future work)."""
    km = distance_km(room["latitude"], room["longitude"],
                     university["latitude"], university["longitude"])
    return round(km * 3 + 5)


def find_matches(profile, university, rooms):
    """Filter the rooms by the mandatory wishes, then score and sort them."""
    matches = []

    for room in rooms:
        minutes = commute_minutes(room, university)

        # --- mandatory requirements: if one fails the room is dropped ---
        if room["city"] != university["city"]:
            continue
        if room["monthly_rent"] > profile["max_rent"]:
            continue
        if room["monthly_rent"] + room["deposit"] > profile["max_upfront"]:
            continue
        if room["room_type"] != profile["room_type"]:
            continue
        if profile["furnished"] and not room["furnished"]:
            continue
        if room["available_from"] > profile["arrival_date"]:
            continue
        if room["available_until"] < profile["end_date"]:
            continue
        if minutes > profile["max_commute"]:
            continue

        # --- score: 65 for passing everything, up to 35 extra points ---
        score = 65
        reasons = []

        if profile["furnished"]:
            score += 15
            reasons.append({"code": "furnished"})

        reasons.append({"code": "room_" + room["room_type"].lower()})

        saving = profile["max_rent"] - room["monthly_rent"]
        if room["monthly_rent"] <= profile["max_rent"] * 0.90:
            score += 10
            reasons.append({"code": "rent", "saving": round(saving),
                            "max": round(profile["max_rent"])})

        reasons.append({"code": "commute", "minutes": minutes,
                        "max": profile["max_commute"]})
        if minutes <= profile["max_commute"] * 0.75:
            score += 10

        reasons.append({"code": "dates"})

        match = dict(room)
        match["commute_minutes"] = minutes
        match["match_score"] = score
        match["match_reasons"] = reasons
        matches.append(match)

    # best score first, cheaper rooms first when the score is equal
    matches.sort(key=lambda m: (-m["match_score"], m["monthly_rent"]))
    return matches
