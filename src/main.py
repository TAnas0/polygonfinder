from fastapi import FastAPI
from .database import SessionLocal, engine
from .models import Base

app = FastAPI()


# Create the database tables
Base.metadata.create_all(bind=engine)  # TODO replace with Alembic migrations


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the PolygonFinder API"}
