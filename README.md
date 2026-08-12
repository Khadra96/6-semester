# VoltEdge Mobility

Dette projekt er udviklet i forbindelse med vores eksamen på 6. semester. Formålet har været at udvikle en MVP, som kan hjælpe VoltEdge Mobility med at opdage mulige fejl på virksomhedens ladestandere.

Løsningen modtager telemetridata fra ladestanderne og vurderer risikoen for fejl ud fra blandt andet status, temperatur, spænding, antal fejl og manglende heartbeat. Hvis risikoniveauet er højt, bliver der automatisk oprettet et incident.

## Løsningens dataflow

Når API’et modtager en telemetrimåling, bliver dataene først valideret. Herefter beregnes en risikoscore, og resultatet gemmes sammen med telemetridataene i PostgreSQL.

Ved høj risiko oprettes der automatisk et incident. De gemte oplysninger kan efterfølgende hentes gennem API’et.

Projektet indeholder desuden et datasæt til Power BI. Dashboardet viser blandt andet temperaturudvikling, ladestandernes status, risikoniveauer og antal incidents.

I denne MVP beregnes risikoen med faste regler. Det gør beregningen let at følge og gør det muligt at afprøve hele dataflowet. En senere version kan anvende en trænet machine learning-model.

## Teknologier

Projektet anvender:

- Python og FastAPI til API’et
- Pydantic til validering af telemetridata
- PostgreSQL til lagring af data
- SQLAlchemy til kommunikationen med databasen
- Docker Compose til at starte databasen
- Pytest til test af løsningen
- GitHub Actions til automatisk at køre testene ved push
- Power BI til visualisering af data

## API

API-dokumentationen kan åbnes gennem Swagger:

```text
http://127.0.0.1:8000/docs