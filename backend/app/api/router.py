from fastapi import APIRouter

from app.api.health import router as health_router
from app.auth.routes import router as auth_router
from app.bids.routes import router as bids_router
from app.checkpoints.routes import router as checkpoints_router
from app.organizations.routes import router as organizations_router
from app.tenders.routes import router as tenders_router
from app.documents.routes import router as documents_router


api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(organizations_router)
api_router.include_router(tenders_router)
api_router.include_router(checkpoints_router)
api_router.include_router(bids_router)
api_router.include_router(documents_router)