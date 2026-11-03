from flask import Blueprint, jsonify, request, session

from student import create_student_profile


student_routes = Blueprint(
    "student_routes",
    __name__
)


@student_routes.post("/api/student-profile")
def student_profile():

    user_id = session.get("user_id")

    if not user_id:

        return jsonify({
            "error": "You must be logged in."
        }), 401

    data = request.json

    if not data:

        return jsonify({
            "error": "No data provided."
        }), 400

    try:

        create_student_profile(
            user_id=user_id,
            university=data.get("university"),
            arrival_date=data["arrival_date"],
            required_until=data.get("required_until"),
            max_rent=data["max_rent"],
            max_upfront_budget=data.get("max_upfront_budget"),
            room_type=data["room_type"],
            furnished=data.get("furnished", False),
            max_commute_minutes=data.get("max_commute_minutes")
        )

        return jsonify({
            "success": True
        }), 201

    except KeyError as error:

        return jsonify({
            "error": f"Missing field: {error.args[0]}"
        }), 400