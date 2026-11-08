import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from application import create_application, update_application_status


def test_application_is_created_for_available_accommodation():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = {"id": 5}

    with patch("application.get_db", return_value=mock_db):
        result = create_application(student_id=1, accommodation_id=5)

    assert result is True
    assert mock_db.execute.call_count == 2
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


def test_application_is_rejected_for_unavailable_accommodation():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = None

    with patch("application.get_db", return_value=mock_db):
        result = create_application(student_id=1, accommodation_id=5)

    assert result is False
    assert mock_db.execute.call_count == 1
    mock_db.commit.assert_not_called()
    mock_db.close.assert_called_once()


def test_application_status_can_be_updated():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = {"id": 10}

    with patch("application.get_db", return_value=mock_db):
        result = update_application_status(
            provider_id=2,
            application_id=10,
            status="ACCEPTED"
        )

    assert result is True
    assert mock_db.execute.call_count == 2
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


def test_invalid_application_status_is_rejected():
    with patch("application.get_db") as mock_get_db:
        result = update_application_status(
            provider_id=2,
            application_id=10,
            status="PENDING"
        )

    assert result is False
    mock_get_db.assert_not_called()