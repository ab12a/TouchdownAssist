from flask import Blueprint, jsonify, request, session

from arrival import (
    get_arrival_tasks,
    update_arrival_task
)


arrival_routes = Blueprint(
    "arrival_routes",
    __name__
)


@arrival_routes.get("/api/arrival-tasks")
def arrival_tasks():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "You must be logged in."
        }), 401

    tasks = get_arrival_tasks(user_id)

    return jsonify({
        "tasks": tasks
    })


@arrival_routes.patch("/api/arrival-tasks/<int:task_id>")
def update_task(task_id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "You must be logged in."
        }), 401

    data = request.json

    if not data or "completed" not in data:
        return jsonify({
            "error": "Completed status is required."
        }), 400

    success = update_arrival_task(
        user_id,
        task_id,
        data["completed"]
    )

    if not success:
        return jsonify({
            "error": "Arrival task not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "Arrival task updated."
    })