import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.risk_service import FailureRiskAssessmentService


INPUT_FILE = PROJECT_ROOT / "data" / "sample_telemetry.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "powerbi_dashboard_data.csv"


def generate_dashboard_data():
    dashboard_rows = []

    with INPUT_FILE.open("r", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)

        for row in reader:
            risk_assessment = FailureRiskAssessmentService.calculate_risk(
                charger_status=row["status"],
                temperature=float(row["temperature"]),
                voltage=float(row["voltage"]),
                error_count=int(row["error_count"]),
                heartbeat_missing=row["heartbeat_missing"].lower() == "true",
            )

            dashboard_rows.append(
                {
                    **row,
                    "risk_score": risk_assessment["risk_score"],
                    "risk_level": risk_assessment["risk_level"],
        "incident_created": risk_assessment["incident_created"],
                        }
            )

    fieldnames = [
        "timestamp",
        "charger_id",
        "connector_id",
        "status",
        "temperature",
        "voltage",
        "error_count",
        "heartbeat_missing",
        "risk_score",
        "risk_level",
        "incident_created",
    ]

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dashboard_rows)

    print(f"Power BI data created: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_dashboard_data()