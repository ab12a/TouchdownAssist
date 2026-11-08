import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from accommodation import create_listing, get_accommodations


def test_accommodation_listing_is_created():
    mock_db = MagicMock()
    mock_db.execute.return_value.lastrowid = 10

    with patch("accommodation.get_db", return_value=mock_db):
        result = create_listing(
            provider_id=1,
            title="Student Room",
            description="Furnished room",
            address="Example Street 1",
            city="Hamburg",
            monthly_rent=600,
            deposit=1000,
            room_type="PRIVATE",
            furnished=1,
            available_from="2026-09-01",
            available_until="2027-06-30",
            commute_minutes=25
        )

    assert result == 10
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


def test_accommodations_can_be_filtered_by_city_and_rent():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchall.return_value = [
        {
            "id": 1,
            "title": "Hamburg Student Room",
            "city": "Hamburg",
            "monthly_rent": 600
        }
    ]

    with patch("accommodation.get_db", return_value=mock_db):
        results = get_accommodations(
            city="Hamburg",
            max_rent=700
        )

    query, parameters = mock_db.execute.call_args[0]

    assert "city = ?" in query
    assert "monthly_rent <= ?" in query
    assert parameters == ["Hamburg", 700]
    assert len(results) == 1
    assert results[0]["title"] == "Hamburg Student Room"
    mock_db.close.assert_called_once()


def test_unfurnished_filter_accepts_false():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchall.return_value = []

    with patch("accommodation.get_db", return_value=mock_db):
        results = get_accommodations(furnished=0)

    query, parameters = mock_db.execute.call_args[0]

    assert "furnished = ?" in query
    assert parameters == [0]
    assert results == []


def test_accommodations_can_be_filtered_by_availability_date():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchall.return_value = []

    with patch("accommodation.get_db", return_value=mock_db):
        get_accommodations(available_on="2026-10-01")

    query, parameters = mock_db.execute.call_args[0]

    assert "available_from <= ?" in query
    assert "available_until >= ?" in query
    assert parameters == ["2026-10-01", "2026-10-01"]
    mock_db.close.assert_called_once()