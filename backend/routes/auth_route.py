from flask import Blueprint, jsonify, request, session

from auth import create_user, login_user


auth_routes = Blueprint(
    "auth_routes",
    __name__
)


@auth_routes.post("/api/register")
def register():

    data = request.json

    try:

        user_id = create_user(
            data["name"],
            data["email"],
            data["password"],
            data["role"]
        )

        return jsonify({
            "success": True,
            "user_id": user_id
        }), 201

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 400


@auth_routes.post("/api/login")
def login():

    data = request.json

    user = login_user(
        data["email"],
        data["password"]
    )

    if not user:

        return jsonify({
            "error": "Invalid email or password."
        }), 401

    session["user_id"] = user["id"]

    return jsonify({
        "success": True,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    })