from sqlalchemy import select
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

    @staticmethod
    def get_recent_telemetry(database: Session) -> list[dict]:
        records = database.scalars(
            select(TelemetryReadingModel)
            .order_by(TelemetryReadingModel.id.desc())
            .limit(100)
        ).all()

        return [
            {
                "id": record.id,
                "charger_id": record.charger_id,
                "connector_id": record.connector_id,
                "status": record.status,
                "temperature": record.temperature,
                "voltage": record.voltage,
                "error_count": record.error_count,
                "heartbeat_missing": record.heartbeat_missing,
                "received_at": record.received_at,
            }
            for record in records
        ]

    @staticmethod
    def get_risk_assessments(database: Session) -> list[dict]:
        records = database.scalars(
            select(RiskAssessmentModel)
            .order_by(RiskAssessmentModel.id.desc())
            .limit(100)
        ).all()

        return [
            {
                "id": record.id,
                "telemetry_id": record.telemetry_id,
                "charger_id": record.charger_id,
                "risk_score": record.risk_score,
                "risk_level": record.risk_level,
                "assessed_at": record.assessed_at,
            }
            for record in records
        ]

    @staticmethod
    def get_open_incidents(database: Session) -> list[dict]:
        records = database.scalars(
            select(IncidentModel)
            .where(IncidentModel.status == "open")
            .order_by(IncidentModel.id.desc())
            .limit(100)
        ).all()

        return [
            {
                "id": record.id,
                "risk_assessment_id": record.risk_assessment_id,
                "charger_id": record.charger_id,
                "priority": record.priority,
                "status": record.status,
                "created_at": record.created_at,
            }
            for record in records
        ]