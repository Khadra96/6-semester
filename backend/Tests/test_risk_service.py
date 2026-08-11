from backend.risk_service import FailureRiskAssessmentService


def test_low_risk_does_not_create_incident():
    result = FailureRiskAssessmentService.calculate_risk(
        charger_status="available",
        temperature=25,
        voltage=230,
        error_count=0,
        heartbeat_missing=False,
    )

    assert result["risk_score"] == 0.0
    assert result["risk_level"] == "Low"
    assert result["incident_created"] is False


def test_high_risk_creates_incident():
    result = FailureRiskAssessmentService.calculate_risk(
        charger_status="faulted",
        temperature=78.5,
        voltage=224,
        error_count=4,
        heartbeat_missing=True,
    )

    assert result["risk_score"] == 1.0
    assert result["risk_level"] == "High"
    assert result["incident_created"] is True
            