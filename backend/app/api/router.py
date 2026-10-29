from fastapi import APIRouter

from app.api.routes.cases import router as cases_router
from app.api.routes.health import router as health_router
from app.api.routes.readiness import router as readiness_router
from app.api.routes.evidence import router as evidence_router
from app.api.routes.observations import router as observations_router
from app.api.routes.scenarios import router as scenarios_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(cases_router, tags=["cases"])
api_router.include_router(evidence_router, tags=["evidence"])
api_router.include_router(readiness_router, tags=["analysis readiness"])
api_router.include_router(observations_router, tags=["observations"])
api_router.include_router(scenarios_router, tags=["scenarios"])
