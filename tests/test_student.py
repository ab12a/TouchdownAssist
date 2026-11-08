
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "backend")
)

from student import create_student_profile


def test_student_profile_is_created():
    mock_db = MagicMock()

    # No existing profile is found
    mock_db.execute.return_value.fetchone.return_value = None

    with patch("student.get_db", return_value=mock_db):
        create_student_profile(
            user_id=1,
            university="University of Hamburg",
            arrival_date="2026-09-01",
            required_until="2027-06-30",
            max_rent=700,
            max_upfront_budget=1500,
            room_type="PRIVATE",
            furnished=True,
            max_commute_minutes=40
        )

    # Verify that the database insert was committed
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()

    # Verify that an INSERT statement was executed
    insert_call = mock_db.execute.call_args_list[1]
    assert "INSERT INTO student_profiles" in insert_call[0][0]

    # Verify that furnished=True was stored as 1
    assert insert_call[0][1][7] == 1
    
