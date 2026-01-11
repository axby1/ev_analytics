from fastapi import FastAPI

from app.api.v1.vehicles import router as vehicles_router

app = FastAPI(title="EV Analytics API")

app.include_router(vehicles_router, prefix="/api/v1")
