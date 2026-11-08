import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from saved import (
    save_accommodation,
    remove_saved_accommodation,
    get_saved_accommodations
)


def test_accommodation_is_saved():
    mock_db = MagicMock()

    with patch("saved.get_db", return_value=mock_db):
        save_accommodation(user_id=1, accommodation_id=5)

    mock_db.execute.assert_called_once()
    assert "INSERT OR IGNORE INTO saved_accommodations" in mock_db.execute.call_args[0][0]
    assert mock_db.execute.call_args[0][1] == (1, 5)
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


def test_saved_accommodation_is_removed():
    mock_db = MagicMock()

    with patch("saved.get_db", return_value=mock_db):
        remove_saved_accommodation(user_id=1, accommodation_id=5)

    mock_db.execute.assert_called_once()
    assert "DELETE FROM saved_accommodations" in mock_db.execute.call_args[0][0]
    assert mock_db.execute.call_args[0][1] == (1, 5)
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


def test_saved_accommodations_are_returned():
    mock_db = MagicMock()

    mock_db.execute.return_value.fetchall.return_value = [
        {
            "id": 5,
            "title": "Student Room",
            "city": "Hamburg",
            "monthly_rent": 600
        }
    ]

    with patch("saved.get_db", return_value=mock_db):
        results = get_saved_accommodations(user_id=1)

    assert len(results) == 1
    assert results[0]["title"] == "Student Room"
    assert results[0]["city"] == "Hamburg"
    mock_db.close.assert_called_once()