import os
from flask import Flask, jsonify
from flask_cors import CORS

from database import init_db

from routes.auth_route import auth_routes
from routes.accomodation_routes import accommodation_routes
from routes.student_route import student_routes
from routes.match_route import match_routes
from routes.saved_route import saved_routes
from routes.application_route import application_routes
from routes.arrival_route import arrival_routes
from routes.university_route import university_routes


app = Flask(__name__)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "local-development-key"
)

CORS(
    app,
    supports_credentials=True
)


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "StudentStay"
    })


app.register_blueprint(auth_routes)
app.register_blueprint(accommodation_routes)
app.register_blueprint(student_routes)
app.register_blueprint(match_routes)
app.register_blueprint(saved_routes)
app.register_blueprint(application_routes)
app.register_blueprint(arrival_routes)
app.register_blueprint(university_routes)


if __name__ == "__main__":
    init_db()
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )