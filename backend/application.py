from database import get_db


def create_application(student_id, accommodation_id):
    db = get_db()

    try:
        # Make sure the accommodation exists and is available.
        accommodation = db.execute(
            """
            SELECT id
            FROM accommodations
            WHERE id = ?
            AND status = 'AVAILABLE'
            """,
            (accommodation_id,)
        ).fetchone()

        if not accommodation:
            return False

        db.execute(
            """
            INSERT INTO applications (
                student_id,
                accommodation_id
            )
            VALUES (?, ?)
            """,
            (student_id, accommodation_id)
        )

        db.commit()
        return True

    except Exception:
        return False

    finally:
        db.close()


def get_student_applications(student_id):
    db = get_db()

    try:
        applications = db.execute(
            """
            SELECT
                ap.id,
                ap.accommodation_id,
                ap.status,
                ap.created_at,
                a.title,
                a.city,
                a.monthly_rent
            FROM applications ap
            JOIN accommodations a
                ON a.id = ap.accommodation_id
            WHERE ap.student_id = ?
            ORDER BY ap.created_at DESC
            """,
            (student_id,)
        ).fetchall()

        return [dict(application) for application in applications]

    finally:
        db.close()


def get_provider_applications(provider_id):
    db = get_db()

    try:
        applications = db.execute(
            """
            SELECT
                ap.id,
                ap.status,
                ap.created_at,
                a.id AS accommodation_id,
                a.title,
                a.city,
                a.monthly_rent,
                u.id AS student_id,
                u.name AS student_name,
                u.email AS student_email
            FROM applications ap
            JOIN accommodations a
                ON a.id = ap.accommodation_id
            JOIN users u
                ON u.id = ap.student_id
            WHERE a.provider_id = ?
            ORDER BY ap.created_at DESC
            """,
            (provider_id,)
        ).fetchall()

        return [dict(application) for application in applications]

    finally:
        db.close()


def update_application_status(
    provider_id,
    application_id,
    status
):
    if status not in ("ACCEPTED", "REJECTED"):
        return False

    db = get_db()

    try:
        application = db.execute(
            """
            SELECT ap.id
            FROM applications ap
            JOIN accommodations a
                ON a.id = ap.accommodation_id
            WHERE ap.id = ?
            AND a.provider_id = ?
            """,
            (application_id, provider_id)
        ).fetchone()

        if not application:
            return False

        db.execute(
            """
            UPDATE applications
            SET status = ?
            WHERE id = ?
            """,
            (status, application_id)
        )

        db.commit()
        return True

    finally:
        db.close()