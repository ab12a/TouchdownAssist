from database import get_db


DEFAULT_TASKS = [
    (
        "Accommodation confirmed",
        "Confirm your accommodation and keep the relevant booking or agreement details."
    ),
    (
        "University registration",
        "Complete the required registration steps with your university."
    ),
    (
        "Registration-related task",
        "Complete the relevant local registration task after arriving."
    ),
    (
        "Bank account",
        "Arrange a suitable bank account if you need one for your studies or accommodation."
    ),
    (
        "Health insurance",
        "Make sure your required health insurance arrangements are in place."
    )
]


def initialize_arrival_tasks(user_id):
    db = get_db()

    try:
        for task_name, description in DEFAULT_TASKS:
            db.execute(
                """
                INSERT OR IGNORE INTO arrival_tasks (
                    user_id,
                    task_name,
                    description
                )
                VALUES (?, ?, ?)
                """,
                (
                    user_id,
                    task_name,
                    description
                )
            )

        db.commit()

    finally:
        db.close()


def get_arrival_tasks(user_id):
    initialize_arrival_tasks(user_id)

    db = get_db()

    try:
        tasks = db.execute(
            """
            SELECT
                id,
                task_name,
                description,
                completed,
                created_at
            FROM arrival_tasks
            WHERE user_id = ?
            ORDER BY id
            """,
            (user_id,)
        ).fetchall()

        return [dict(task) for task in tasks]

    finally:
        db.close()


def update_arrival_task(
    user_id,
    task_id,
    completed
):
    db = get_db()

    try:
        cursor = db.execute(
            """
            UPDATE arrival_tasks
            SET completed = ?
            WHERE id = ?
            AND user_id = ?
            """,
            (
                1 if completed else 0,
                task_id,
                user_id
            )
        )

        db.commit()

        return cursor.rowcount > 0

    finally:
        db.close()
