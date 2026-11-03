from flask import Blueprint, jsonify, session

from saved import (
    save_accommodation,
    remove_saved_accommodation,
    get_saved_accommodations
)


saved_routes = Blueprint(
    "saved_routes",
    __name__
)


@saved_routes.post("/api/saved/<int:accommodation_id>")
def save(accommodation_id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "You must be logged in."
        }), 401

    save_accommodation(
        user_id,
        accommodation_id
    )

    return jsonify({
        "success": True,
        "message": "Accommodation saved."
    })


@saved_routes.delete("/api/saved/<int:accommodation_id>")
def remove(accommodation_id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "You must be logged in."
        }), 401

    remove_saved_accommodation(
        user_id,
        accommodation_id
    )

    return jsonify({
        "success": True,
        "message": "Accommodation removed from saved list."
    })


@saved_routes.get("/api/saved")
def saved():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "You must be logged in."
        }), 401

    accommodations = get_saved_accommodations(user_id)

    return jsonify({
        "accommodations": accommodations
    })