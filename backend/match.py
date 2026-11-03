from database import get_db


def get_student_profile(user_id):
    db = get_db()

    try:
        profile = db.execute(
            """
            SELECT
                sp.university,
                u.city AS university_city,
                sp.arrival_date,
                sp.required_until,
                sp.max_rent,
                sp.max_upfront_budget,
                sp.room_type,
                sp.furnished,
                sp.max_commute_minutes
            FROM student_profiles sp
            LEFT JOIN universities u
                ON sp.university = u.name
            WHERE sp.user_id = ?
            """,
            (user_id,)
        ).fetchone()

        if not profile:
            return None

        return dict(profile)

    finally:
        db.close()


def find_matches(user_id):
    profile = get_student_profile(user_id)

    if not profile:
        return []

    db = get_db()

    try:
        listings = db.execute(
            """
            SELECT
                id,
                title,
                description,
                address,
                city,
                monthly_rent,
                deposit,
                room_type,
                furnished,
                available_from,
                available_until,
                commute_minutes,
                status
            FROM accommodations
            WHERE status = 'AVAILABLE'
            """
        ).fetchall()

        matches = []

        for listing in listings:

            # -------------------------------------------------
            # LOCATION
            # -------------------------------------------------

            if profile["university_city"]:
                if (
                    listing["city"].strip().lower()
                    != profile["university_city"].strip().lower()
                ):
                    continue

            # -------------------------------------------------
            # HARD REQUIREMENTS
            # -------------------------------------------------

            # Maximum monthly rent
            if profile["max_rent"] is not None:
                if listing["monthly_rent"] > profile["max_rent"]:
                    continue

            # Room type
            if profile["room_type"]:
                required_room = profile["room_type"].strip().upper()
                listing_room = listing["room_type"].strip().upper()

                if listing_room != required_room:
                    continue

            # Furnished requirement
            if profile["furnished"]:
                if not listing["furnished"]:
                    continue

            # Available by arrival date
            if profile["arrival_date"]:
                if listing["available_from"] > profile["arrival_date"]:
                    continue

            # Available for the complete required period
            if (
                profile["required_until"]
                and listing["available_until"]
            ):
                if listing["available_until"] < profile["required_until"]:
                    continue

            # Maximum commute
            if (
                profile["max_commute_minutes"] is not None
                and listing["commute_minutes"] is not None
            ):
                if (
                    listing["commute_minutes"]
                    > profile["max_commute_minutes"]
                ):
                    continue

            # -------------------------------------------------
            # MATCH SCORE
            # -------------------------------------------------

            score = 65
            reasons = []

            # Furnished bonus
            if profile["furnished"] and listing["furnished"]:
                score += 15

            # Below maximum rent bonus
            if profile["max_rent"] is not None:

                affordable_limit = profile["max_rent"] * 0.90

                if listing["monthly_rent"] <= affordable_limit:

                    score += 10

            # Short commute bonus
            if (
                profile["max_commute_minutes"] is not None
                and listing["commute_minutes"] is not None
            ):

                short_commute_limit = (
                    profile["max_commute_minutes"] * 0.75
                )

                if listing["commute_minutes"] <= short_commute_limit:
                    score += 10

            # -------------------------------------------------
            # MAIN MATCH REASONS
            # -------------------------------------------------

            # Room type and furnishing
            if profile["room_type"] and profile["furnished"]:
                reasons.append(
                    f"{profile['room_type'].lower().capitalize()}, "
                    "furnished room as requested"
                )

            elif profile["room_type"]:
                reasons.append(
                    f"Matches your "
                    f"{profile['room_type'].lower()} room requirement"
                )

            elif profile["furnished"]:
                reasons.append(
                    "Furnished accommodation"
                )

            # Rent
            if profile["max_rent"] is not None:

                savings = (
                    profile["max_rent"]
                    - listing["monthly_rent"]
                )

                reasons.append(
                    f"€{savings:.0f} below your "
                    f"€{profile['max_rent']:.0f} maximum rent"
                )

            # Commute
            if (
                profile["max_commute_minutes"] is not None
                and listing["commute_minutes"] is not None
            ):
                reasons.append(
                    f"{listing['commute_minutes']}-minute commute "
                    f"within your "
                    f"{profile['max_commute_minutes']}-minute limit"
                )

            # Availability
            if (
                profile["arrival_date"]
                and profile["required_until"]
            ):
                reasons.append(
                    "Available for your required dates"
                )

            elif profile["arrival_date"]:
                reasons.append(
                    "Available by your arrival date"
                )

            elif profile["required_until"]:
                reasons.append(
                    "Available until your required date"
                )

            # -------------------------------------------------
            # BUILD RESULT
            # -------------------------------------------------

            match = dict(listing)

            match["match_score"] = score
            match["match_reasons"] = reasons

            matches.append(match)

        # Highest matching score first
        matches.sort(
            key=lambda accommodation: accommodation["match_score"],
            reverse=True
        )

        return matches

    finally:
        db.close()