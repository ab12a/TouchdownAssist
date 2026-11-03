from database import get_db


def create_student_profile(
    user_id,
    university,
    arrival_date,
    required_until,
    max_rent,
    max_upfront_budget,
    room_type,
    furnished,
    max_commute_minutes
):
    db = get_db()

    try:
        existing_profile = db.execute(
            """
            SELECT id
            FROM student_profiles
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        if existing_profile:
            # Profile already exists, so update it.
            db.execute(
                """
                UPDATE student_profiles
                SET
                    university = ?,
                    arrival_date = ?,
                    required_until = ?,
                    max_rent = ?,
                    max_upfront_budget = ?,
                    room_type = ?,
                    furnished = ?,
                    max_commute_minutes = ?
                WHERE user_id = ?
                """,
                (
                    university,
                    arrival_date,
                    required_until,
                    max_rent,
                    max_upfront_budget,
                    room_type,
                    1 if furnished else 0,
                    max_commute_minutes,
                    user_id
                )
            )

        else:
            # No profile exists yet, so create one.
            db.execute(
                """
                INSERT INTO student_profiles (
                    user_id,
                    university,
                    arrival_date,
                    required_until,
                    max_rent,
                    max_upfront_budget,
                    room_type,
                    furnished,
                    max_commute_minutes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    university,
                    arrival_date,
                    required_until,
                    max_rent,
                    max_upfront_budget,
                    room_type,
                    1 if furnished else 0,
                    max_commute_minutes
                )
            )

        db.commit()

    finally:
        db.close()