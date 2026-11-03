from flask import Blueprint, jsonify, session

from match import find_matches


match_routes = Blueprint(
    "match_routes",
    __name__
)


@match_routes.get("/api/matches")
def matches():

    user_id = session.get("user_id")

    if not user_id:

        return jsonify({
            "error": "You must be logged in."
        }), 401

    results = find_matches(user_id)

    return jsonify({
        "matches": results
    })