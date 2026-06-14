from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.infrastructure.database.database import get_db
from app.domain.models.unidade import Unidade
from app.core.dependencies import permitir_perfis

from app.schema.unidade_schema import (
    UnidadeCreate,
    UnidadeUpdate,
    UnidadeResponse
)

router = APIRouter(tags=["Unidades"])

# Rota para criar uma nova unidade.
@router.post(
    "/unidades",
    response_model=UnidadeResponse,
    status_code=201
)
def criar_unidade(
    unidade: UnidadeCreate,
    db: Session = Depends(get_db),
    usuario_logado = Depends(
        permitir_perfis(["ADMIN", "GERENTE"])
    )
):

    nova_unidade = Unidade(
        nome=unidade.nome,
        cidade=unidade.cidade,
        estado=unidade.estado,
        status=unidade.status
    )

    db.add(nova_unidade)

    db.commit()

    db.refresh(nova_unidade)

    return nova_unidade

# Rota para listar todas as unidades ativas
@router.get(
    "/unidades",
    response_model=list[UnidadeResponse]
)
def listar_unidades(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10 # Limite de 10 itens por página, conforme regra de negócios.
):
    offset = (page - 1) * limit

    unidades = db.query(Unidade).filter(
        Unidade.status == "ATIVO"
    ).offset(offset).limit(limit).all()

    return unidades

# Rota para buscar uma unidade por ID
@router.get(
    "/unidades/{idUnidade}",
    response_model=UnidadeResponse
)
def buscar_unidade(
    idUnidade: int,
    db: Session = Depends(get_db)
):

    unidade = db.query(Unidade).filter(
        Unidade.idUnidade == idUnidade
    ).first()

    if not unidade:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    return unidade

# Rota para atualizar uma unidade
@router.put(
    "/unidades/{idUnidade}",
    response_model=UnidadeResponse
)
def atualizar_unidade(
    idUnidade: int,
    dados: UnidadeUpdate,
    db: Session = Depends(get_db),
    usuario_logado = Depends(
        permitir_perfis(["ADMIN", "GERENTE"])
    )
):

    unidade = db.query(Unidade).filter(
        Unidade.idUnidade == idUnidade
    ).first()

    if not unidade:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    unidade.nome = dados.nome
    unidade.cidade = dados.cidade
    unidade.estado = dados.estado
    unidade.status = dados.status

    db.commit()

    db.refresh(unidade)

    return unidade

# Rota para inativar uma unidade
@router.delete(
    "/unidades/{idUnidade}",
    status_code=200
)
def inativar_unidade(
    idUnidade: int,
    db: Session = Depends(get_db),
    usuario_logado = Depends(
        permitir_perfis(["ADMIN"])
    )
):

    unidade = db.query(Unidade).filter(
        Unidade.idUnidade == idUnidade
    ).first()

    if not unidade:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    unidade.status = "INATIVO"

    db.commit()

    return {
        "message": "Unidade inativada com sucesso"
    }