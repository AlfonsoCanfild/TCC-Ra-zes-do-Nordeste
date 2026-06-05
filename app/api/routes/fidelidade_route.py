from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

from app.domain.models.fidelidade import Fidelidade

from app.schema.fidelidade_schema import (
    FidelidadeResponse
)

router = APIRouter(tags=["Fidelidade"]) # Roteador para as rotas relacionadas ao programa de fidelidade dos usuários


# Rotas para o programa de fidelidade dos usuários
@router.get(
    "/fidelidade/{idUsuario}",
    response_model=FidelidadeResponse
)
def consultar_fidelidade(
    idUsuario: int,
    db: Session = Depends(get_db)
):

    fidelidade = db.query(Fidelidade).filter(
        Fidelidade.idUsuario == idUsuario
    ).first()

    if not fidelidade: # Se o usuário não tiver um programa de fidelidade, retorna um erro 404
        raise HTTPException(
            status_code=404,
            detail="Cliente não possui pontos"
        )

    return fidelidade


# Rota para listar o programa de fidelidade de todos os usuários
@router.get(
    "/fidelidade",
    response_model=list[FidelidadeResponse]
)
def listar_fidelidade(
    db: Session = Depends(get_db)
):

    return db.query(Fidelidade).all()