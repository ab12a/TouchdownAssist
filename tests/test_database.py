import os
import tempfile
import unittest
from unittest.mock import patch

import database


def count(table):
    return database.query("SELECT COUNT(*) AS n FROM " + table)[0]["n"]


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        # every test gets a new empty database file
        path = os.path.join(tempfile.mkdtemp(), "db_test.db")
        patcher = patch.object(database, "DATABASE", path)
        patcher.start()
        self.addCleanup(patcher.stop)
        database.init_db()

    def test_tables_are_created(self):
        names = [row["name"] for row in
                 database.query("SELECT name FROM sqlite_master WHERE type = 'table'")]
        for table in ["users", "universities", "accommodations", "profiles",
                      "saved", "interests", "tasks"]:
            self.assertIn(table, names)

    def test_sample_data_is_inserted(self):
        self.assertGreater(count("universities"), 0)
        self.assertGreater(count("accommodations"), 0)

    def test_second_init_does_not_duplicate_data(self):
        universities, rooms, users = count("universities"), count("accommodations"), count("users")
        database.init_db()
        self.assertEqual(count("universities"), universities)
        self.assertEqual(count("accommodations"), rooms)
        self.assertEqual(count("users"), users)  # demo user is not added twice

    def test_every_university_city_has_rooms(self):
        # otherwise a student of this university would never get a match
        cities = database.query(
            "SELECT DISTINCT u.city FROM universities u "
            "LEFT JOIN accommodations a ON a.city = u.city WHERE a.id IS NULL")
        self.assertEqual(cities, [])

    def test_demo_user_exists_with_hashed_password(self):
        user = database.query("SELECT * FROM users WHERE email = ?", (database.DEMO_EMAIL,))[0]
        self.assertNotEqual(user["password_hash"], database.DEMO_PASSWORD)
        self.assertEqual(count("tasks"), 5)

    def test_failed_insert_does_not_lock_the_database(self):
        before = count("users")
        database.execute("INSERT INTO users (name, email, password_hash) VALUES ('A', 'a@a.com', 'x')")
        with self.assertRaises(Exception):
            database.execute("INSERT INTO users (name, email, password_hash) VALUES ('B', 'a@a.com', 'x')")
        # a second write must still work (this was a real bug once)
        database.execute("INSERT INTO users (name, email, password_hash) VALUES ('C', 'c@c.com', 'x')")
        self.assertEqual(count("users"), before + 2)


if __name__ == "__main__":
    unittest.main()
