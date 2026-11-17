import os
import sqlite3
from datetime import date

from flask import Flask, jsonify, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from database import TASK_KEYS, execute, init_db, query
from matching import find_matches

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-development-key")

init_db()  # runs on start-up, so it also works inside Docker

# these API paths can be used without being logged in
OPEN_PATHS = ["/api/login", "/api/register", "/api/universities", "/api/health"]


def error(message, status):
    return jsonify({"error": message}), status


@app.before_request
def check_login():
    if request.path.startswith("/api/") and request.path not in OPEN_PATHS:
        if "user_id" not in session:
            return error("Please log in.", 401)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "TouchdownAssist"})


@app.get("/")
def home():
    return render_template("index.html")


# ---------- login / register ----------

@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not name:
        return error("name_missing", 400)
    if "@" not in email:
        return error("email_invalid", 400)
    if len(password) < 6:
        return error("password_short", 400)

    try:
        user_id = execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, generate_password_hash(password))).lastrowid
    except sqlite3.IntegrityError:  # email is UNIQUE
        return error("email_taken", 400)

    for key in TASK_KEYS:
        execute("INSERT INTO tasks (user_id, task_key) VALUES (?, ?)", (user_id, key))

    session["user_id"] = user_id
    return jsonify({"name": name}), 201


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    users = query("SELECT * FROM users WHERE email = ?", (email,))
    if not users or not check_password_hash(users[0]["password_hash"], password):
        return error("Wrong email or password.", 401)

    session["user_id"] = users[0]["id"]
    return jsonify({"name": users[0]["name"]})


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.get("/api/me")
def me():
    users = query("SELECT name FROM users WHERE id = ?", (session["user_id"],))
    if not users:  # user was deleted but the cookie is still there
        session.clear()
        return error("Please log in.", 401)
    return jsonify({"name": users[0]["name"]})


# ---------- universities and profile ----------

@app.get("/api/universities")
def universities():
    return jsonify(query("SELECT * FROM universities ORDER BY city, name"))


def read_profile(data):
    """Check the profile from the browser. Returns a dict or None if invalid."""
    try:
        profile = {
            "university_id": int(data["university_id"]),
            "arrival_date": str(data["arrival_date"]),
            "end_date": str(data["end_date"]),
            "max_rent": float(data["max_rent"]),
            "max_upfront": float(data["max_upfront"]),
            "max_commute": int(data["max_commute"]),
            "room_type": str(data["room_type"]).upper(),
            "furnished": 1 if data["furnished"] else 0,
        }
        date.fromisoformat(profile["arrival_date"])  # raises ValueError if wrong
        date.fromisoformat(profile["end_date"])
    except (KeyError, ValueError, TypeError):
        return None

    if profile["room_type"] not in ("PRIVATE", "SHARED"):
        return None
    if profile["arrival_date"] > profile["end_date"]:
        return None
    if min(profile["max_rent"], profile["max_upfront"], profile["max_commute"]) <= 0:
        return None
    if not query("SELECT id FROM universities WHERE id = ?", (profile["university_id"],)):
        return None
    return profile


@app.get("/api/profile")
def get_profile():
    rows = query("SELECT * FROM profiles WHERE user_id = ?", (session["user_id"],))
    return jsonify(rows[0] if rows else None)


@app.post("/api/profile")
def save_profile():
    profile = read_profile(request.get_json(silent=True) or {})
    if profile is None:
        return error("Invalid profile.", 400)

    execute(
        "INSERT OR REPLACE INTO profiles (user_id, university_id, arrival_date, end_date, "
        "max_rent, max_upfront, max_commute, room_type, furnished) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (session["user_id"], profile["university_id"], profile["arrival_date"],
         profile["end_date"], profile["max_rent"], profile["max_upfront"],
         profile["max_commute"], profile["room_type"], profile["furnished"]))
    return jsonify({"ok": True})


# ---------- matching ----------

@app.get("/api/matches")
def matches():
    profiles = query("SELECT * FROM profiles WHERE user_id = ?", (session["user_id"],))
    if not profiles:
        return jsonify([])

    university = query("SELECT * FROM universities WHERE id = ?",
                       (profiles[0]["university_id"],))[0]
    rooms = query("SELECT * FROM accommodations")
    return jsonify(find_matches(profiles[0], university, rooms))


# ---------- saved accommodations and expressions of interest ----------

def room_exists(accommodation_id):
    return len(query("SELECT id FROM accommodations WHERE id = ?", (accommodation_id,))) > 0


@app.get("/api/saved")
def get_saved():
    return jsonify(query(
        "SELECT a.* FROM accommodations a JOIN saved s ON s.accommodation_id = a.id "
        "WHERE s.user_id = ?", (session["user_id"],)))


@app.post("/api/saved/<int:accommodation_id>")
def save_room(accommodation_id):
    if not room_exists(accommodation_id):
        return error("Accommodation not found.", 404)
    execute("INSERT OR IGNORE INTO saved (user_id, accommodation_id) VALUES (?, ?)",
            (session["user_id"], accommodation_id))
    return jsonify({"ok": True}), 201


@app.delete("/api/saved/<int:accommodation_id>")
def remove_saved(accommodation_id):
    execute("DELETE FROM saved WHERE user_id = ? AND accommodation_id = ?",
            (session["user_id"], accommodation_id))
    return jsonify({"ok": True})


@app.get("/api/interest")
def get_interests():
    rows = query("SELECT accommodation_id FROM interests WHERE user_id = ?",
                 (session["user_id"],))
    return jsonify([row["accommodation_id"] for row in rows])


@app.post("/api/interest/<int:accommodation_id>")
def send_interest(accommodation_id):
    if not room_exists(accommodation_id):
        return error("Accommodation not found.", 404)
    execute("INSERT OR IGNORE INTO interests (user_id, accommodation_id) VALUES (?, ?)",
            (session["user_id"], accommodation_id))
    return jsonify({"ok": True}), 201


# ---------- arrival planner ----------

@app.get("/api/tasks")
def get_tasks():
    return jsonify(query("SELECT id, task_key, done FROM tasks WHERE user_id = ? ORDER BY id",
                         (session["user_id"],)))


@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    if "done" not in data:
        return error("Missing field: done", 400)

    cursor = execute("UPDATE tasks SET done = ? WHERE id = ? AND user_id = ?",
                     (1 if data["done"] else 0, task_id, session["user_id"]))
    if cursor.rowcount == 0:
        return error("Task not found.", 404)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
