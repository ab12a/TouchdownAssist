from database import get_db


def save_accommodation(user_id, accommodation_id):
    db = get_db()

    try:
        db.execute(
            """
            INSERT OR IGNORE INTO saved_accommodations (
                user_id,
                accommodation_id
            )
            VALUES (?, ?)
            """,
            (user_id, accommodation_id)
        )

        db.commit()

    finally:
        db.close()


def remove_saved_accommodation(user_id, accommodation_id):
    db = get_db()

    try:
        db.execute(
            """
            DELETE FROM saved_accommodations
            WHERE user_id = ?
            AND accommodation_id = ?
            """,
            (user_id, accommodation_id)
        )

        db.commit()

    finally:
        db.close()


def get_saved_accommodations(user_id):
    db = get_db()

    try:
        listings = db.execute(
            """
            SELECT
                a.id,
                a.title,
                a.description,
                a.address,
                a.city,
                a.monthly_rent,
                a.deposit,
                a.room_type,
                a.furnished,
                a.available_from,
                a.available_until,
                a.commute_minutes,
                a.status
            FROM saved_accommodations s
            JOIN accommodations a
                ON a.id = s.accommodation_id
            WHERE s.user_id = ?
            ORDER BY s.created_at DESC
            """,
            (user_id,)
        ).fetchall()

        return [dict(listing) for listing in listings]

    finally:
        db.close()
