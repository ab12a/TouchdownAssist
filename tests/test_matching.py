
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Allow tests to import modules from the backend folder
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "backend")
)

from match import find_matches


def make_profile(**overrides):
    profile = {
        "university": "University of Hamburg",
        "university_city": "Hamburg",
        "arrival_date": "2026-09-01",
        "required_until": "2027-06-30",
        "max_rent": 700,
        "max_upfront_budget": 1500,
        "room_type": "PRIVATE",
        "furnished": 1,
        "max_commute_minutes": 40
    }
    profile.update(overrides)
    return profile


def make_listing(**overrides):
    listing = {
        "id": 1,
        "title": "Student Room",
        "description": "A furnished student room",
        "address": "Example Street 1",
        "city": "Hamburg",
        "monthly_rent": 600,
        "deposit": 1000,
        "room_type": "PRIVATE",
        "furnished": 1,
        "available_from": "2026-08-01",
        "available_until": "2027-07-31",
        "commute_minutes": 25,
        "status": "AVAILABLE"
    }
    listing.update(overrides)
    return listing


def run_matching(profile, listings):
    mock_db = MagicMock()

    # First database query returns the accommodation listings
    mock_db.execute.return_value.fetchall.return_value = listings

    with patch("match.get_student_profile", return_value=profile), \
         patch("match.get_db", return_value=mock_db):
        return find_matches(1)


def test_suitable_accommodation_is_returned():
    results = run_matching(
        make_profile(),
        [make_listing()]
    )

    assert len(results) == 1
    assert results[0]["title"] == "Student Room"


def test_accommodation_above_maximum_rent_is_excluded():
    results = run_matching(
        make_profile(max_rent=700),
        [make_listing(monthly_rent=750)]
    )

    assert results == []


def test_wrong_room_type_is_excluded():
    results = run_matching(
        make_profile(room_type="PRIVATE"),
        [make_listing(room_type="SHARED")]
    )

    assert results == []


def test_matches_are_sorted_by_score():
    cheaper_room = make_listing(
        id=1,
        title="Cheaper Room",
        monthly_rent=500,
        commute_minutes=20
    )

    standard_room = make_listing(
        id=2,
        title="Standard Room",
        monthly_rent=650,
        commute_minutes=35
    )

    results = run_matching(
        make_profile(),
        [standard_room, cheaper_room]
    )

    assert len(results) == 2
    assert results[0]["title"] == "Cheaper Room"
    assert results[0]["match_score"] >= results[1]["match_score"]
