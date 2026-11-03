from database import get_db


def create_listing(
    provider_id,
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
    commute_minutes=None
):
    db = get_db()

    try:
        cursor = db.execute(
            """
            INSERT INTO accommodations (
                provider_id,
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
                commute_minutes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                provider_id,
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
                commute_minutes
            )
        )

        db.commit()
        return cursor.lastrowid

    finally:
        db.close()


def get_accommodations(
    city=None,
    max_rent=None,
    room_type=None,
    furnished=None,
    available_on=None
):
    db = get_db()

    try:
        query = """
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

        parameters = []

        if city:
            query += " AND city = ?"
            parameters.append(city)

        if max_rent is not None:
            query += " AND monthly_rent <= ?"
            parameters.append(max_rent)

        if room_type:
            query += " AND room_type = ?"
            parameters.append(room_type)

        if furnished is not None:
            query += " AND furnished = ?"
            parameters.append(furnished)

        if available_on:
            query += """
                AND available_from <= ?
                AND (
                    available_until IS NULL
                    OR available_until >= ?
                )
            """
            parameters.append(available_on)
            parameters.append(available_on)

        query += " ORDER BY id DESC"

        listings = db.execute(
            query,
            parameters
        ).fetchall()

        return [dict(listing) for listing in listings]

    finally:
        db.close()