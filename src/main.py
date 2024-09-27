from fastapi import FastAPI
from .routes import router

app = FastAPI()

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the PolygonFinder API"}
