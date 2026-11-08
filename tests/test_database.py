import sys
import sqlite3
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "backend")
)

import database


def test_database_tables_are_created(tmp_path, monkeypatch):
    db_path = tmp_path / "test_studentstay.db"
    monkeypatch.setattr(database, "DATABASE", str(db_path))

    database.init_db()

    db = database.get_db()

    try:
        tables = {
            row["name"]
            for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }

        expected_tables = {
            "users",
            "accommodations",
            "student_profiles",
            "saved_accommodations",
            "applications",
            "arrival_tasks",
            "universities"
        }

        assert expected_tables.issubset(tables)

    finally:
        db.close()


def test_universities_are_inserted(tmp_path, monkeypatch):
    db_path = tmp_path / "test_studentstay.db"
    monkeypatch.setattr(database, "DATABASE", str(db_path))

    database.init_db()

    db = database.get_db()

    try:
        count = db.execute(
            "SELECT COUNT(*) FROM universities"
        ).fetchone()[0]

        assert count > 0

    finally:
        db.close()


def test_sample_accommodations_are_inserted(tmp_path, monkeypatch):
    db_path = tmp_path / "test_studentstay.db"
    monkeypatch.setattr(database, "DATABASE", str(db_path))

    database.init_db()

    db = database.get_db()

    try:
        count = db.execute(
            "SELECT COUNT(*) FROM accommodations"
        ).fetchone()[0]

        assert count > 0

    finally:
        db.close()


def test_initialization_does_not_create_duplicate_data(
    tmp_path, monkeypatch
):
    db_path = tmp_path / "test_studentstay.db"
    monkeypatch.setattr(database, "DATABASE", str(db_path))

    database.init_db()

    db = database.get_db()

    try:
        first_university_count = db.execute(
            "SELECT COUNT(*) FROM universities"
        ).fetchone()[0]

        first_accommodation_count = db.execute(
            "SELECT COUNT(*) FROM accommodations"
        ).fetchone()[0]

    finally:
        db.close()

    database.init_db()

    db = database.get_db()

    try:
        second_university_count = db.execute(
            "SELECT COUNT(*) FROM universities"
        ).fetchone()[0]

        second_accommodation_count = db.execute(
            "SELECT COUNT(*) FROM accommodations"
        ).fetchone()[0]

        assert second_university_count == first_university_count
        assert second_accommodation_count == first_accommodation_count

    finally:
        db.close()