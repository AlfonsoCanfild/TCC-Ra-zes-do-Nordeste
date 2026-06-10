from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.core.dependencies import permitir_perfis
from app.domain.models.fidelidade import Fidelidade

from app.schema.fidelidade_schema import (
    FidelidadeResponse
)

router = APIRouter(tags=["Fidelidade"]) # Roteador para as rotas relacionadas ao programa de fidelidade dos usuários

# As rotas de fidelidade permitem listar os pontos de fidelidade dos usuários.
@router.get(
    "/fidelidade",
    response_model=list[FidelidadeResponse]
)
def listar_fidelidade(
    db: Session = Depends(get_db),
    usuario = Depends(
        permitir_perfis(
            ["ADMIN", "GERENTE"]
        )
    )
):

    return db.query(Fidelidade).all()


# Rota para listar os usuários com mais pontos de fidelidade
@router.get(
    "/fidelidade/ranking",
    response_model=list[FidelidadeResponse]
)
def ranking_fidelidade(
    db: Session = Depends(get_db),
    usuario = Depends(
        permitir_perfis(
            ["ADMIN", "GERENTE"]
        )
    )
):

    return db.query(Fidelidade).order_by(
        Fidelidade.pontos.desc()
    ).all()


# Rota para buscar os pontos de fidelidade de um usuário específico, acessível apenas para perfis ADMIN e GERENTE
@router.get(
    "/fidelidade/{idUsuario}",
    response_model=FidelidadeResponse
)
def buscar_fidelidade(
    idUsuario: int,
    db: Session = Depends(get_db),
    usuario = Depends(
        permitir_perfis(
            ["ADMIN", "GERENTE"]
        )
    )
):

    fidelidade = db.query(Fidelidade).filter(
        Fidelidade.idUsuario == idUsuario
    ).first()

    if not fidelidade:
        raise HTTPException(
            status_code=404,
            detail="Cliente não possui pontos"
        )

    return fidelidade