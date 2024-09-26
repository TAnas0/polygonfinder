from fastapi import FastAPI
from .database import engine
from .models import Base

app = FastAPI()


# Create the database tables
Base.metadata.create_all(bind=engine)  # TODO replace with Alembic migrations


@app.get("/")
async def read_root():
    return {"message": "Welcome to the PolygonFinder API"}
