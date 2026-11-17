import os
import sqlite3

from werkzeug.security import generate_password_hash

DATABASE = os.environ.get("TOUCHDOWN_DB", "touchdownassist.db")

# the arrival planner tasks every student gets (texts are in static/app.js)
TASK_KEYS = ["accommodation", "university", "registration", "bank", "insurance"]


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def query(sql, args=()):
    """Run a SELECT and return a list of dicts."""
    db = get_db()
    try:
        return [dict(row) for row in db.execute(sql, args).fetchall()]
    finally:
        db.close()  # always close, otherwise a failed query can keep the db locked


def execute(sql, args=()):
    """Run an INSERT/UPDATE/DELETE. Returns the cursor (lastrowid, rowcount)."""
    db = get_db()
    try:
        cursor = db.execute(sql, args)
        db.commit()
        return cursor
    finally:
        db.close()


TABLES = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS universities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    city TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS accommodations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    monthly_rent REAL NOT NULL,
    deposit REAL NOT NULL,
    room_type TEXT NOT NULL,          -- PRIVATE or SHARED
    furnished INTEGER NOT NULL,       -- 1 or 0
    available_from TEXT NOT NULL,     -- dates as YYYY-MM-DD
    available_until TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS profiles (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    university_id INTEGER NOT NULL REFERENCES universities(id),
    arrival_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    max_rent REAL NOT NULL,
    max_upfront REAL NOT NULL,
    max_commute INTEGER NOT NULL,
    room_type TEXT NOT NULL,
    furnished INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS saved (
    user_id INTEGER NOT NULL REFERENCES users(id),
    accommodation_id INTEGER NOT NULL REFERENCES accommodations(id),
    PRIMARY KEY (user_id, accommodation_id)
);
CREATE TABLE IF NOT EXISTS interests (
    user_id INTEGER NOT NULL REFERENCES users(id),
    accommodation_id INTEGER NOT NULL REFERENCES accommodations(id),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, accommodation_id)
);
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    task_key TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0,
    UNIQUE (user_id, task_key)
);
"""

# name, city, latitude, longitude
UNIVERSITIES = [
    ("RWTH Aachen University", "Aachen", 50.777, 6.077),
    ("FH Aachen", "Aachen", 50.7753, 6.0839),
    ("Freie Universität Berlin", "Berlin", 52.453, 13.29),
    ("Humboldt-Universität zu Berlin", "Berlin", 52.517, 13.393),
    ("Technische Universität Berlin", "Berlin", 52.5125, 13.3269),
    ("HTW Berlin", "Berlin", 52.456, 13.525),
    ("University of Bonn", "Bonn", 50.7339, 7.102),
    ("University of Bremen", "Bremen", 53.1067, 8.852),
    ("University of Cologne", "Cologne", 50.928, 6.928),
    ("TH Köln", "Cologne", 50.939, 6.956),
    ("TU Darmstadt", "Darmstadt", 49.873, 8.655),
    ("TU Dresden", "Dresden", 51.028, 13.728),
    ("Heinrich Heine University Düsseldorf", "Düsseldorf", 51.189, 6.795),
    ("Goethe University Frankfurt", "Frankfurt", 50.127, 8.667),
    ("Frankfurt University of Applied Sciences", "Frankfurt", 50.132, 8.696),
    ("University of Freiburg", "Freiburg", 48.0, 7.842),
    ("Universität Hamburg", "Hamburg", 53.5669, 9.984),
    ("HAW Hamburg", "Hamburg", 53.557, 10.022),
    ("TU Hamburg", "Hamburg", 53.461, 9.969),
    ("Leibniz University Hannover", "Hannover", 52.382, 9.717),
    ("Heidelberg University", "Heidelberg", 49.4108, 8.706),
    ("Karlsruhe Institute of Technology", "Karlsruhe", 49.009, 8.413),
    ("Kiel University", "Kiel", 54.342, 10.122),
    ("Leipzig University", "Leipzig", 51.339, 12.373),
    ("University of Mannheim", "Mannheim", 49.483, 8.462),
    ("Ludwig-Maximilians-Universität München", "Munich", 48.1508, 11.5802),
    ("Technische Universität München", "Munich", 48.1497, 11.5673),
    ("University of Münster", "Münster", 51.963, 7.62),
    ("FAU Erlangen-Nürnberg", "Nuremberg", 49.452, 11.082),
    ("University of Stuttgart", "Stuttgart", 48.748, 9.106),
    ("FH Wedel", "Wedel", 53.5833, 9.7167),
]

# normal monthly rent for a private furnished room, other cities use 480
CITY_RENT = {"Munich": 700, "Hamburg": 560, "Berlin": 600, "Frankfurt": 600,
             "Stuttgart": 600, "Cologne": 560}

# room type, furnished, rent factor, free from, free until, (lat, lon) shift
# The shift moves the room a bit away from the city centre, so that the
# commute is different for every room and every university.
ROOM_TYPES = [
    ("PRIVATE", 1, 1.00, "2026-09-15", "2027-09-30", (0.020, 0.010)),
    ("PRIVATE", 0, 0.92, "2026-10-01", "2027-03-31", (-0.030, 0.020)),
    ("SHARED", 1, 0.75, "2026-09-20", "2027-09-30", (0.010, -0.030)),
    ("SHARED", 0, 0.68, "2026-10-15", "2027-03-31", (-0.020, -0.040)),
]


# demo account so a marker can log in without registering (listed in README.md)
DEMO_NAME = "Demo Student"
DEMO_EMAIL = "student@test.com"
DEMO_PASSWORD = "password123"


def seed_demo_user(db):
    if db.execute("SELECT id FROM users WHERE email = ?", (DEMO_EMAIL,)).fetchone():
        return
    cursor = db.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                        (DEMO_NAME, DEMO_EMAIL, generate_password_hash(DEMO_PASSWORD)))
    for key in TASK_KEYS:
        db.execute("INSERT INTO tasks (user_id, task_key) VALUES (?, ?)", (cursor.lastrowid, key))


def seed(db):
    """Fill the university and accommodation tables the first time."""
    if db.execute("SELECT COUNT(*) FROM universities").fetchone()[0] == 0:
        db.executemany("INSERT INTO universities (name, city, latitude, longitude) "
                       "VALUES (?, ?, ?, ?)", UNIVERSITIES)

    if db.execute("SELECT COUNT(*) FROM accommodations").fetchone()[0] > 0:
        return

    centres = db.execute("SELECT city, AVG(latitude) AS lat, AVG(longitude) AS lon "
                         "FROM universities GROUP BY city").fetchall()
    for centre in centres:
        base_rent = CITY_RENT.get(centre["city"], 480)
        for room_type, furnished, factor, free_from, free_until, shift in ROOM_TYPES:
            rent = round(base_rent * factor)
            db.execute(
                "INSERT INTO accommodations (city, latitude, longitude, monthly_rent, "
                "deposit, room_type, furnished, available_from, available_until) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (centre["city"], centre["lat"] + shift[0], centre["lon"] + shift[1],
                 rent, rent * 2, room_type, furnished, free_from, free_until))


def init_db():
    db = get_db()
    db.executescript(TABLES)
    seed(db)
    seed_demo_user(db)
    db.commit()
    db.close()
