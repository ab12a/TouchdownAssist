import os
import tempfile
import unittest

# use an empty temporary database, set BEFORE the app is imported
os.environ["TOUCHDOWN_DB"] = os.path.join(tempfile.mkdtemp(), "test.db")

from app import app  # noqa: E402

PROFILE = {
    "university_id": 3,  # Freie Universität Berlin
    "arrival_date": "2026-09-20", "end_date": "2027-03-31",
    "max_rent": 700, "max_upfront": 2000, "max_commute": 40,
    "room_type": "PRIVATE", "furnished": True,
}


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()  # every test gets its own session cookie

    def register(self, email="anna@test.com"):
        return self.client.post("/api/register", json={
            "name": "Anna", "email": email, "password": "secret123"})

    def test_not_logged_in(self):
        self.assertEqual(self.client.get("/api/matches").status_code, 401)

    def test_register_and_login(self):
        self.assertEqual(self.register("a1@test.com").status_code, 201)
        self.client.post("/api/logout")
        ok = self.client.post("/api/login", json={"email": "a1@test.com", "password": "secret123"})
        self.assertEqual(ok.status_code, 200)

    def test_demo_account_can_log_in(self):
        ok = self.client.post("/api/login", json={"email": "student@test.com", "password": "password123"})
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(len(self.client.get("/api/tasks").get_json()), 5)

    def test_wrong_password(self):
        self.register("a2@test.com")
        self.client.post("/api/logout")
        bad = self.client.post("/api/login", json={"email": "a2@test.com", "password": "wrong"})
        self.assertEqual(bad.status_code, 401)

    def test_duplicate_email_and_bad_input_do_not_crash(self):
        self.register("a3@test.com")
        self.assertEqual(self.register("a3@test.com").status_code, 400)
        self.assertEqual(self.client.post("/api/login").status_code, 401)  # no body at all
        self.assertEqual(self.client.post("/api/register", json={}).status_code, 400)

    def test_register_errors_say_what_is_wrong(self):
        def error_of(**changes):
            body = {"name": "Anna", "email": "e1@test.com", "password": "secret123"}
            body.update(changes)
            return self.client.post("/api/register", json=body).get_json()["error"]

        self.assertEqual(error_of(name=""), "name_missing")
        self.assertEqual(error_of(email="no-at-sign"), "email_invalid")
        self.assertEqual(error_of(password="123"), "password_short")
        self.register("e2@test.com")
        self.assertEqual(error_of(email="e2@test.com"), "email_taken")

    def test_password_is_not_stored_as_plain_text(self):
        from database import query
        self.register("a4@test.com")
        stored = query("SELECT password_hash FROM users WHERE email = 'a4@test.com'")[0]["password_hash"]
        self.assertNotIn("secret123", stored)

    def test_profile_and_matches(self):
        self.register("a5@test.com")
        self.assertEqual(self.client.post("/api/profile", json=PROFILE).status_code, 200)
        matches = self.client.get("/api/matches").get_json()
        self.assertGreater(len(matches), 0)
        self.assertTrue(all(m["city"] == "Berlin" for m in matches))
        scores = [m["match_score"] for m in matches]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_invalid_profile_is_rejected(self):
        self.register("a6@test.com")
        bad = dict(PROFILE, max_rent="abc")
        self.assertEqual(self.client.post("/api/profile", json=bad).status_code, 400)

    def test_save_and_remove(self):
        self.register("a7@test.com")
        self.assertEqual(self.client.post("/api/saved/1").status_code, 201)
        self.assertEqual(len(self.client.get("/api/saved").get_json()), 1)
        self.client.delete("/api/saved/1")
        self.assertEqual(len(self.client.get("/api/saved").get_json()), 0)

    def test_unknown_accommodation_gives_404(self):
        self.register("a8@test.com")
        self.assertEqual(self.client.post("/api/saved/99999").status_code, 404)
        self.assertEqual(self.client.post("/api/interest/99999").status_code, 404)

    def test_expression_of_interest(self):
        self.register("a9@test.com")
        self.assertEqual(self.client.post("/api/interest/1").status_code, 201)
        self.assertEqual(self.client.get("/api/interest").get_json(), [1])

    def test_arrival_tasks(self):
        self.register("b1@test.com")
        tasks = self.client.get("/api/tasks").get_json()
        self.assertEqual(len(tasks), 5)
        self.client.patch("/api/tasks/%d" % tasks[0]["id"], json={"done": True})
        self.assertEqual(self.client.get("/api/tasks").get_json()[0]["done"], 1)
        self.assertEqual(self.client.patch("/api/tasks/99999", json={"done": True}).status_code, 404)

    def test_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_universities_are_public(self):
        universities = self.client.get("/api/universities").get_json()
        self.assertGreater(len(universities), 0)

    def test_logout_ends_the_session(self):
        self.register("c1@test.com")
        self.assertEqual(self.client.get("/api/me").status_code, 200)
        self.client.post("/api/logout")
        self.assertEqual(self.client.get("/api/me").status_code, 401)

    def test_profile_can_be_updated(self):
        self.register("c2@test.com")
        self.client.post("/api/profile", json=PROFILE)
        self.client.post("/api/profile", json=dict(PROFILE, max_rent=550, room_type="SHARED"))
        saved = self.client.get("/api/profile").get_json()
        self.assertEqual(saved["max_rent"], 550)
        self.assertEqual(saved["room_type"], "SHARED")

    def test_profile_with_arrival_after_end_is_rejected(self):
        self.register("c3@test.com")
        bad = dict(PROFILE, arrival_date="2027-05-01", end_date="2027-01-01")
        self.assertEqual(self.client.post("/api/profile", json=bad).status_code, 400)

    def test_matches_without_profile_are_empty(self):
        self.register("c4@test.com")
        self.assertEqual(self.client.get("/api/matches").get_json(), [])

    def test_interest_twice_is_stored_once(self):
        self.register("c5@test.com")
        self.client.post("/api/interest/2")
        self.client.post("/api/interest/2")
        self.assertEqual(self.client.get("/api/interest").get_json(), [2])

    def test_saving_twice_is_stored_once(self):
        self.register("c6@test.com")
        self.client.post("/api/saved/2")
        self.client.post("/api/saved/2")
        self.assertEqual(len(self.client.get("/api/saved").get_json()), 1)

    def test_user_cannot_change_tasks_of_another_user(self):
        self.register("c7@test.com")
        task_id = self.client.get("/api/tasks").get_json()[0]["id"]

        other = app.test_client()
        other.post("/api/register", json={"name": "Ben", "email": "c8@test.com", "password": "secret123"})
        self.assertEqual(other.patch("/api/tasks/%d" % task_id, json={"done": True}).status_code, 404)
        self.assertEqual(self.client.get("/api/tasks").get_json()[0]["done"], 0)


if __name__ == "__main__":
    unittest.main()
