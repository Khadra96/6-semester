from sqlalchemy.orm import Session

from backend.models import (
    IncidentModel,
    RiskAssessmentModel,
    TelemetryReadingModel,
)


class TelemetryRepository:
    @staticmethod
    def save_telemetry_flow(
        database: Session,
        telemetry,
        risk_assessment: dict,
    ) -> dict:
        try:
            telemetry_record = TelemetryReadingModel(
                charger_id=telemetry.charger_id,
                connector_id=telemetry.connector_id,
                status=telemetry.status,
                temperature=telemetry.temperature,
                voltage=telemetry.voltage,
                error_count=telemetry.error_count,
                heartbeat_missing=telemetry.heartbeat_missing,
            )

            database.add(telemetry_record)
            database.flush()

            risk_record = RiskAssessmentModel(
                telemetry_id=telemetry_record.id,
                charger_id=telemetry.charger_id,
                risk_score=risk_assessment["risk_score"],
                risk_level=risk_assessment["risk_level"],
            )

            database.add(risk_record)
            database.flush()

            incident_id = None

            if risk_assessment["incident_created"]:
                incident_record = IncidentModel(
                    risk_assessment_id=risk_record.id,
                    charger_id=telemetry.charger_id,
                    priority="High",
                    status="open",
                )

                database.add(incident_record)
                database.flush()
                incident_id = incident_record.id

            database.commit()

            return {
                "telemetry_id": telemetry_record.id,
                "risk_assessment_id": risk_record.id,
                "incident_id": incident_id,
            }

        except Exception:
            database.rollback()
            raise