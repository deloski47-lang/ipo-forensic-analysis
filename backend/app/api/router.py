from fastapi import APIRouter

from app.api.routes.cases import router as cases_router
from app.api.routes.health import router as health_router
from app.api.routes.evidence import router as evidence_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(cases_router, tags=["cases"])
api_router.include_router(evidence_router, tags=["evidence"])
