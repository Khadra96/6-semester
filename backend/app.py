from typing import Literal

from fastapi import FastAPI, status
from pydantic import BaseModel, Field


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
def receive_telemetry(telemetry: TelemetryReading):
    return {
        "message": "Telemetry accepted",
        "data": telemetry,
    }