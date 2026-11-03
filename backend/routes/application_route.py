from flask import Blueprint, jsonify, session, request

from application import (
    create_application,
    get_student_applications,
    get_provider_applications,
    update_application_status
)


application_routes = Blueprint(
    "application_routes",
    __name__
)


@application_routes.post("/api/applications/<int:accommodation_id>")
def apply(accommodation_id):
    student_id = session.get("user_id")

    if not student_id:
        return jsonify({
            "error": "You must be logged in."
        }), 401

    success = create_application(
        student_id,
        accommodation_id
    )

    if not success:
        return jsonify({
            "error": "Unable to submit application. "
                     "The accommodation may not be available "
                     "or you may have already applied."
        }), 400

    return jsonify({
        "success": True,
        "message": "Application submitted."
    }), 201


@application_routes.get("/api/applications")
def applications():
    student_id = session.get("user_id")

    if not student_id:
        return jsonify({
            "error": "You must be logged in."
        }), 401

    results = get_student_applications(
        student_id
    )

    return jsonify({
        "applications": results
    })


@application_routes.get("/api/provider/applications")
def provider_applications():
    provider_id = session.get("user_id")

    if not provider_id:
        return jsonify({
            "error": "You must be logged in."
        }), 401

    results = get_provider_applications(
        provider_id
    )

    return jsonify({
        "applications": results
    })


@application_routes.patch("/api/provider/applications/<int:application_id>")
def update_status(application_id):
    provider_id = session.get("user_id")

    if not provider_id:
        return jsonify({
            "error": "You must be logged in."
        }), 401

    data = request.json

    if not data or "status" not in data:
        return jsonify({
            "error": "Status is required."
        }), 400

    success = update_application_status(
        provider_id,
        application_id,
        data["status"]
    )

    if not success:
        return jsonify({
            "error": "Unable to update application."
        }), 400

    return jsonify({
        "success": True,
        "message": "Application status updated."
    })