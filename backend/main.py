from fastapi import FastAPI
from database import engine, Base
from routes.events import router as events_router

app = FastAPI(title="SaaS Churn Intelligence API")

Base.metadata.create_all(bind=engine)

app.include_router(events_router)

@app.get("/health")
def health():
    return {"status": "healthy"}
