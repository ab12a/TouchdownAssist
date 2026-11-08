
import sys
from pathlib import Path

# Allow tests to import modules from the backend folder
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "backend")
)

from auth import hash_password, verify_password


def test_correct_password_is_verified():
    password = "StudentTest123!"

    stored_password = hash_password(password)

    assert verify_password(password, stored_password) is True


def test_incorrect_password_is_rejected():
    password = "StudentTest123!"

    stored_password = hash_password(password)

    assert verify_password("WrongPassword123!", stored_password) is False
