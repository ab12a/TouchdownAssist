import hashlib
import secrets
from database import get_db


def hash_password(password):

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        120000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_password):

    salt_hex, hash_hex = stored_password.split(":")

    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(hash_hex)

    actual = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        120000
    )

    return secrets.compare_digest(
        actual,
        expected
    )


def create_user(name, email, password, role):

    db = get_db()

    password_hash = hash_password(password)

    try:

        cursor = db.execute(
            """
            INSERT INTO users
            (name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email.lower(),
                password_hash,
                role
            )
        )

        db.commit()

        return cursor.lastrowid

    finally:

        db.close()


def login_user(email, password):

    db = get_db()

    user = db.execute(
        """
        SELECT id, name, email, password_hash, role
        FROM users
        WHERE email = ?
        """,
        (email.lower(),)
    ).fetchone()

    db.close()

    if not user:
        return None

    if not verify_password(
        password,
        user["password_hash"]
    ):
        return None

    return dict(user)