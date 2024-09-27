from fastapi import FastAPI
from .routes import router
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


# Create a Limiter instance
limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
app = FastAPI()

# Register the Limiter middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the PolygonFinder API"}
