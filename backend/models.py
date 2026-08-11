from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class TelemetryReadingModel(Base):
    __tablename__ = "telemetry_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    charger_id: Mapped[str] = mapped_column(String(50), index=True)
    connector_id: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(30))
    temperature: Mapped[float] = mapped_column(Float)
    voltage: Mapped[float] = mapped_column(Float)
    error_count: Mapped[int] = mapped_column(Integer)
    heartbeat_missing: Mapped[bool] = mapped_column(Boolean)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class RiskAssessmentModel(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telemetry_id: Mapped[int] = mapped_column(
        ForeignKey("telemetry_readings.id")
    )
    charger_id: Mapped[str] = mapped_column(String(50), index=True)
    risk_score: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(20))
    assessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class IncidentModel(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    risk_assessment_id: Mapped[int] = mapped_column(
        ForeignKey("risk_assessments.id")
    )
    charger_id: Mapped[str] = mapped_column(String(50), index=True)
    priority: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(
        String(20),
        default="open",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )