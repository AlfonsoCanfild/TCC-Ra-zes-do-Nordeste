from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.core.dependencies import permitir_perfis
from app.domain.models.auditoria import Auditoria

from app.schema.auditoria_schema import (
    AuditoriaResponse
)

router = APIRouter(tags=["Auditoria"])

# Rota para listar as auditorias, acessível apenas para usuários com perfil "ADMIN"
@router.get(
    "/auditoria",
    response_model=list[AuditoriaResponse]
)
def listar_auditoria(
    db: Session = Depends(get_db),
    usuario = Depends(
        permitir_perfis(
            ["ADMIN"]
        )
    )
):

    return db.query(Auditoria).all()

# Rota para buscar uma auditoria por ID, acessível apenas para usuários com perfil "ADMIN"
@router.get(
    "/auditoria/{idAuditoria}",
    response_model=AuditoriaResponse
)
def buscar_auditoria(
    idAuditoria: int,
    db: Session = Depends(get_db),
    usuario = Depends(
        permitir_perfis(
            ["ADMIN"]
        )
    )
):

    auditoria = db.query(Auditoria).filter(
        Auditoria.idAuditoria == idAuditoria
    ).first()

    if not auditoria:
        raise HTTPException(
            status_code=404,
            detail="Registro não encontrado"
        )

    return auditoria