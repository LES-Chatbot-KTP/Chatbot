"""Admin panel routes — metrics and logs."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_admin_user
from app.models.usuario import Usuario
from app.schemas.admin import MetricasResponse, LogAdministrativoResponse
from app.services import admin_service

router = APIRouter(prefix="/api/admin", tags=["Administração"])


@router.get("/metricas", response_model=MetricasResponse)
def get_metricas(
    db: Session = Depends(get_db),
    _admin: Usuario = Depends(get_admin_user),
):
    """Get administrative dashboard metrics (admin only)."""
    return admin_service.get_metricas(db)


@router.get("/logs", response_model=list[LogAdministrativoResponse])
def list_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _admin: Usuario = Depends(get_admin_user),
):
    """List admin activity logs (admin only)."""
    return admin_service.list_logs(db, skip, limit)
