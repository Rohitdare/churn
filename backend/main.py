from fastapi import FastAPI
from database import engine, Base
from routes.events import router as events_router
from routes.customers import router as customers_router


from database import SessionLocal
from models import Event

app = FastAPI(title="SaaS Churn Intelligence API")

Base.metadata.create_all(bind=engine)

app.include_router(events_router)
app.include_router(customers_router)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/debug/events-count")
def events_count():
    db = SessionLocal()
    count = db.query(Event).count()
    db.close()
    return {"events": count}

