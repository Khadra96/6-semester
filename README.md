# VoltEdge Mobility

Dette repository indeholder vores MVP til VoltEdge Mobility. Projektet er udviklet som en del af eksamen på 6. semester.

VoltEdge arbejder med ladestandere fra forskellige leverandører. En af udfordringerne er, at fejl kan være svære at opdage, før en ladestander allerede er ude af drift. Derfor har vi lavet en løsning, som modtager telemetridata og vurderer, hvor stor risiko der er for en fejl.

Hvis risikoen er høj, opretter systemet automatisk et incident, så VoltEdge kan reagere hurtigere.

### Sådan fungerer løsningen

Når API’et modtager telemetridata fra en ladestander, sker der følgende:

1. Dataene bliver valideret.
2. Systemet beregner en risikoscore.
3. Telemetridata og risikovurderingen gemmes i PostgreSQL.
4. Hvis risikoen er høj, oprettes der automatisk et incident.
5. De gemte data kan hentes gennem API’et og senere bruges i eksempelvis Power BI.

Risikovurderingen tager blandt andet højde for:

- ladestanderens status
- temperatur
- spænding
- antal registrerede fejl
- manglende heartbeat

I vores MVP bruger vi faste og gennemsigtige regler til at beregne risikoen. Det gør det muligt at demonstrere hele dataflowet. Senere kan denne del udvides med en machine learning-model.

### Teknologier

Vi har anvendt:

- Python og FastAPI til API’et
- Pydantic til validering af data
- PostgreSQL til lagring
- SQLAlchemy til kommunikationen med databasen
- Docker Compose til at starte databasen
- Pytest til automatiserede tests
- GitHub Actions til automatisk test ved push

### API

API-dokumentationen kan ses gennem Swagger på:

```text
http://127.0.0.1:8000/docs
```

API’et indeholder følgende endpoints:

| Metode | Endpoint | Funktion |
|---|---|---|
| GET | `/` | Viser om API’et kører |
| GET | `/health` | Kontrollerer systemets status |
| POST | `/api/telemetry` | Modtager nye telemetridata |
| GET | `/api/telemetry` | Henter gemte telemetridata |
| GET | `/api/risk-assessments` | Henter risikovurderinger |
| GET | `/api/incidents` | Henter åbne incidents |

### Sådan startes projektet

PostgreSQL-databasen startes med:

```powershell
docker compose up -d database
```

Python-pakkerne installeres med:

```powershell
python -m pip install -r backend/requirements.txt
```

API’et startes med:

```powershell
python -m uvicorn backend.app:app --reload
```

Derefter kan Swagger åbnes på `http://127.0.0.1:8000/docs`.

### Tests

Testene køres med:

```powershell
python -m pytest -v
```

Vi tester blandt andet:

- at gyldige telemetridata accepteres
- at ugyldige temperaturer afvises
- at en lav risiko ikke opretter et incident
- at en høj risiko opretter et incident

GitHub Actions kører automatisk testene, når ny kode pushes til GitHub. Det gør det lettere for os at opdage fejl under udviklingen.

### Sikkerhed

Databaseoplysningerne ligger lokalt i `.env` og bliver ikke uploadet til GitHub. `.env.example` viser, hvilke oplysninger der skal udfyldes, uden at indeholde det rigtige password.

### Næste udviklingstrin

MVP’en viser det grundlæggende dataflow fra ladestander til risikovurdering og incident. Næste trin kan være at koble dataene til Power BI og senere erstatte de faste risikoregler med en trænet machine learning-model.