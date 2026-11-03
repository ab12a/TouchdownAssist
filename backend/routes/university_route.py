from flask import Blueprint, jsonify, request
from database import get_db

university_routes = Blueprint(
    "university_routes",
    __name__
)


@university_routes.get("/api/universities")
def get_universities():

    city = request.args.get("city")

    db = get_db()

    try:

        if city:

            universities = db.execute(
                """
                SELECT
                    id,
                    name,
                    city,
                    latitude,
                    longitude
                FROM universities
                WHERE city = ?
                ORDER BY name
                """,
                (city,)
            ).fetchall()

        else:

            universities = db.execute(
                """
                SELECT
                    id,
                    name,
                    city,
                    latitude,
                    longitude
                FROM universities
                ORDER BY city, name
                """
            ).fetchall()


        return jsonify({
            "universities": [
                dict(university)
                for university in universities
            ]
        })


    finally:

        db.close()