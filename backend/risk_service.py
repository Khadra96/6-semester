class FailureRiskAssessmentService:
    HIGH_RISK_THRESHOLD = 0.80

    @staticmethod
    def calculate_risk(
        charger_status: str,
        temperature: float,
        voltage: float,
        error_count: int,
        heartbeat_missing: bool,
    ) -> dict:
        risk_score = 0.0

        if charger_status == "faulted":
            risk_score += 0.40

        if temperature >= 70:
            risk_score += 0.25

        if voltage < 210 or voltage > 250:
            risk_score += 0.10

        risk_score += min(error_count * 0.05, 0.20)

        if heartbeat_missing:
            risk_score += 0.25

        risk_score = min(round(risk_score, 2), 1.0)

        if risk_score >= 0.80:
            risk_level = "High"
        elif risk_score >= 0.50:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "incident_created": (
                risk_score
                >= FailureRiskAssessmentService.HIGH_RISK_THRESHOLD
            ),
        }
    