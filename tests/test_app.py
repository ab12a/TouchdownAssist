import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app import app


def test_flask_application_is_created():
    assert app is not None
    assert app.name == "app"


def test_health_endpoint_returns_ok():
    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "service": "StudentStay"
    }


def test_application_routes_are_registered():
    registered_routes = [
        rule.rule for rule in app.url_map.iter_rules()
    ]

    assert "/api/health" in registered_routes
    assert len(registered_routes) > 1