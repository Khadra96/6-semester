from fastapi.testclient import TestClient

from backend.app import app


client = TestClient(app)


def test_valid_telemetry_is_accepted_and_saved():
    response = client.post(
        "/api/telemetry",
        json={
            "charger_id": "CH-001",
            "connector_id": "CON-01",
            "status": "faulted",
            "temperature": 78.5,
            "voltage": 224,
            "error_count": 4,
            "heartbeat_missing": True,
        },
    )

    assert response.status_code == 201

    result = response.json()

    assert result["message"] == "Telemetry accepted and saved"
    assert result["risk_assessment"]["risk_level"] == "High"
    assert result["risk_assessment"]["incident_created"] is True
    assert result["database_records"]["telemetry_id"] is not None
    assert result["database_records"]["risk_assessment_id"] is not None
    assert result["database_records"]["incident_id"] is not None


def test_invalid_temperature_is_rejected():
    response = client.post(
        "/api/telemetry",
        json={
            "charger_id": "CH-002",
            "connector_id": "CON-01",
            "status": "charging",
            "temperature": 200,
            "voltage": 230,
            "error_count": 0,
            "heartbeat_missing": False,
        },
    )

    assert response.status_code == 422