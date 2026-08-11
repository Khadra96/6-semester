from fastapi import FastAPI

app = FastAPI(
    title="VoltEdge Mobility API",
    description="API til overvågning af ladestandere og telemetridata",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "VoltEdge API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}