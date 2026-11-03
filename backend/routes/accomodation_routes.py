from flask import Blueprint, jsonify, request, session

from accommodation import (
    create_listing,
    get_accommodations
)


accommodation_routes = Blueprint(
    "accommodation_routes",
    __name__
)


@accommodation_routes.post("/api/accommodations")
def add_accommodation():

    data = request.json

    provider_id = session.get("user_id")

    if not provider_id:

        return jsonify({
            "error": "You must be logged in."
        }), 401

    if not data:

        return jsonify({
            "error": "No data provided."
        }), 400

    try:

        listing_id = create_listing(
            provider_id=provider_id,
            title=data["title"],
            description=data.get("description", ""),
            address=data["address"],
            city=data.get("city", ""),
            monthly_rent=data["monthly_rent"],
            deposit=data.get("deposit", 0),
            room_type=data["room_type"],
            furnished=data.get("furnished", False),
            available_from=data["available_from"],
            available_until=data.get("available_until")
        )

        return jsonify({
            "success": True,
            "listing_id": listing_id
        }), 201

    except KeyError as error:

        return jsonify({
            "error": f"Missing field: {error.args[0]}"
        }), 400


@accommodation_routes.get("/api/accommodations")
def accommodations():

    city = request.args.get("city")

    max_rent = request.args.get(
        "max_rent",
        type=float
    )

    room_type = request.args.get("room_type")

    furnished = request.args.get(
        "furnished",
        type=lambda value: value.lower() == "true"
    )

    available_on = request.args.get("available_on")

    listings = get_accommodations(
        city=city,
        max_rent=max_rent,
        room_type=room_type,
        furnished=furnished,
        available_on=available_on
    )

    return jsonify({
        "accommodations": listings
    })