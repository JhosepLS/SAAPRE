from fastapi import APIRouter

from app.api.v1 import admin, analysis, health, models, players

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(players.router)
api_router.include_router(analysis.router)
api_router.include_router(models.router)
api_router.include_router(admin.router)
