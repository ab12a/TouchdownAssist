import unittest

from matching import find_matches

UNIVERSITY = {"city": "Berlin", "latitude": 52.5125, "longitude": 13.3269}

PROFILE = {
    "max_rent": 700, "max_upfront": 2000, "max_commute": 40,
    "room_type": "PRIVATE", "furnished": 1,
    "arrival_date": "2026-09-20", "end_date": "2027-03-31",
}


def make_room(**changes):
    """A room that fits the profile, changed by the given values."""
    room = {
        "id": 1, "city": "Berlin", "latitude": 52.52, "longitude": 13.33,
        "monthly_rent": 600, "deposit": 1200, "room_type": "PRIVATE",
        "furnished": 1, "available_from": "2026-09-15",
        "available_until": "2027-09-30",
    }
    room.update(changes)
    return room


class MatchingTest(unittest.TestCase):

    def test_good_room_is_found(self):
        result = find_matches(PROFILE, UNIVERSITY, [make_room()])
        self.assertEqual(len(result), 1)

    def test_too_expensive_is_removed(self):
        self.assertEqual(find_matches(PROFILE, UNIVERSITY, [make_room(monthly_rent=800)]), [])

    def test_upfront_cost_is_checked(self):
        room = make_room(monthly_rent=690, deposit=1500)  # 2190 > 2000
        self.assertEqual(find_matches(PROFILE, UNIVERSITY, [room]), [])

    def test_wrong_city_is_removed(self):
        self.assertEqual(find_matches(PROFILE, UNIVERSITY, [make_room(city="Munich")]), [])

    def test_wrong_room_type_is_removed(self):
        self.assertEqual(find_matches(PROFILE, UNIVERSITY, [make_room(room_type="SHARED")]), [])

    def test_unfurnished_is_removed_when_furnished_needed(self):
        self.assertEqual(find_matches(PROFILE, UNIVERSITY, [make_room(furnished=0)]), [])

    def test_room_free_too_late_is_removed(self):
        self.assertEqual(find_matches(PROFILE, UNIVERSITY, [make_room(available_from="2026-10-15")]), [])

    def test_room_ends_too_early_is_removed(self):
        self.assertEqual(find_matches(PROFILE, UNIVERSITY, [make_room(available_until="2027-01-31")]), [])

    def test_long_commute_is_removed(self):
        far = make_room(latitude=52.9, longitude=13.9)
        self.assertEqual(find_matches(PROFILE, UNIVERSITY, [far]), [])

    def test_score_is_100_for_a_perfect_room(self):
        # furnished +15, rent under 90% of 700 +10, commute under 30 min +10
        room = make_room(monthly_rent=600)
        self.assertEqual(find_matches(PROFILE, UNIVERSITY, [room])[0]["match_score"], 100)

    def test_score_is_65_when_nothing_extra_fits(self):
        profile = dict(PROFILE, furnished=0)
        room = make_room(furnished=0, monthly_rent=690, latitude=52.58, longitude=13.45)  # about 39 minutes away
        result = find_matches(profile, UNIVERSITY, [room])
        self.assertEqual(result[0]["match_score"], 65)

    def test_best_score_comes_first(self):
        cheap = make_room(id=1, monthly_rent=600)
        dear = make_room(id=2, monthly_rent=690)
        result = find_matches(PROFILE, UNIVERSITY, [dear, cheap])
        self.assertEqual([m["id"] for m in result], [1, 2])

    def test_reasons_are_given(self):
        reasons = find_matches(PROFILE, UNIVERSITY, [make_room()])[0]["match_reasons"]
        codes = [r["code"] for r in reasons]
        self.assertIn("commute", codes)
        self.assertIn("dates", codes)

    def test_same_input_gives_same_result(self):
        rooms = [make_room(id=1), make_room(id=2, monthly_rent=650)]
        self.assertEqual(find_matches(PROFILE, UNIVERSITY, rooms),
                         find_matches(PROFILE, UNIVERSITY, rooms))


if __name__ == "__main__":
    unittest.main()
