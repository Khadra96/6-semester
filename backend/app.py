from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend import models
from backend.database import Base, engine, get_database_session
from backend.repository import TelemetryRepository
from backend.risk_service import FailureRiskAssessmentService


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="VoltEdge Mobility API",
    description="API til overvågning af ladestandere og telemetridata",
    version="1.0.0",
)


class TelemetryReading(BaseModel):
    charger_id: str = Field(min_length=1)
    connector_id: str = Field(min_length=1)
    status: Literal["available", "charging", "faulted", "offline"]
    temperature: float = Field(ge=-40, le=120)
    voltage: float = Field(ge=0, le=500)
    error_count: int = Field(ge=0)
    heartbeat_missing: bool = False


@app.get("/")
def home():
    return {"message": "VoltEdge API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/telemetry", status_code=status.HTTP_201_CREATED)
def receive_telemetry(
    telemetry: TelemetryReading,
    database: Session = Depends(get_database_session),
):
    risk_assessment = FailureRiskAssessmentService.calculate_risk(
        charger_status=telemetry.status,
        temperature=telemetry.temperature,
        voltage=telemetry.voltage,
        error_count=telemetry.error_count,
        heartbeat_missing=telemetry.heartbeat_missing,
    )

    try:
        database_records = TelemetryRepository.save_telemetry_flow(
            database=database,
            telemetry=telemetry,
            risk_assessment=risk_assessment,
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Data could not be saved in the database",
        ) from error

    return {
        "message": "Telemetry accepted and saved",
        "data": telemetry,
        "risk_assessment": risk_assessment,
        "database_records": database_records,
    }


@app.get("/api/telemetry")
def get_telemetry(
    database: Session = Depends(get_database_session),
):
    return TelemetryRepository.get_recent_telemetry(database)


@app.get("/api/risk-assessments")
def get_risk_assessments(
    database: Session = Depends(get_database_session),
):
    return TelemetryRepository.get_risk_assessments(database)


@app.get("/api/incidents")
def get_open_incidents(
    database: Session = Depends(get_database_session),
):
    return TelemetryRepository.get_open_incidents(database)