import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from arrival import (
    DEFAULT_TASKS,
    initialize_arrival_tasks,
    get_arrival_tasks,
    update_arrival_task
)


def test_default_arrival_tasks_are_initialized():
    mock_db = MagicMock()

    with patch("arrival.get_db", return_value=mock_db):
        initialize_arrival_tasks(user_id=1)

    assert mock_db.execute.call_count == len(DEFAULT_TASKS)
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


def test_arrival_tasks_are_returned():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchall.return_value = [
        {
            "id": 1,
            "task_name": "Accommodation confirmed",
            "description": "Confirm your accommodation.",
            "completed": 0,
            "created_at": "2026-09-01"
        }
    ]

    with patch("arrival.get_db", return_value=mock_db):
        results = get_arrival_tasks(user_id=1)

    assert len(results) == 1
    assert results[0]["task_name"] == "Accommodation confirmed"
    assert results[0]["completed"] == 0
    assert mock_db.close.call_count == 2


def test_arrival_task_can_be_marked_complete():
    mock_db = MagicMock()
    mock_db.execute.return_value.rowcount = 1

    with patch("arrival.get_db", return_value=mock_db):
        result = update_arrival_task(
            user_id=1,
            task_id=1,
            completed=True
        )

    assert result is True
    assert mock_db.execute.call_args[0][1] == (1, 1, 1)
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()