from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.infrastructure.database.database import get_db

from app.domain.models.estoque import Estoque
from app.domain.models.produto import Produto
from app.domain.models.unidade import Unidade

from app.schema.estoque_schema import (
    EstoqueCreate,
    EstoqueResponse,
    EstoqueUpdate
)

router = APIRouter(tags=["Estoque"])

# Rota para criar um novo estoque, mas verificando se a unidade e o produto existem antes de criar o estoque.
@router.post(
    "/estoque",
    response_model=EstoqueResponse,
    status_code=201
)
def criar_estoque(
    estoque: EstoqueCreate,
    db: Session = Depends(get_db)
):

    unidade = db.query(Unidade).filter(
        Unidade.idUnidade == estoque.idUnidade
    ).first()

    if not unidade: # Verifica se a unidade existe no banco de dados, se não existir, retorna um erro 404.
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    produto = db.query(Produto).filter(
        Produto.idProduto == estoque.idProduto
    ).first()

    if not produto: # Verifica se o produto existe no banco de dados, se não existir, retorna um erro 404.
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    novo_estoque = Estoque(
        idUnidade=estoque.idUnidade,
        idProduto=estoque.idProduto,
        quantidade=estoque.quantidade
    )

    db.add(novo_estoque)

    db.commit()

    db.refresh(novo_estoque)

    return novo_estoque


# Rota para listar todos os estoques.
@router.get(
    "/estoque",
    response_model=list[EstoqueResponse]
)
def listar_estoque(
    db: Session = Depends(get_db)
):

    estoque = db.query(Estoque).all()

    return estoque


# Rota para buscar um estoque por ID.
@router.get(
    "/estoque/{idEstoque}",
    response_model=EstoqueResponse
)
def buscar_estoque(
    idEstoque: int,
    db: Session = Depends(get_db)
):

    estoque = db.query(Estoque).filter(
        Estoque.idEstoque == idEstoque
    ).first()

    if not estoque:
        raise HTTPException(
            status_code=404,
            detail="Registro de estoque não encontrado"
        )

    return estoque


# Rota para atualizar a quantidade de um estoque.
@router.put(
    "/estoque/{idEstoque}",
    response_model=EstoqueResponse
)
def atualizar_estoque(
    idEstoque: int,
    dados: EstoqueUpdate,
    db: Session = Depends(get_db)
):

    estoque = db.query(Estoque).filter(
        Estoque.idEstoque == idEstoque
    ).first()

    if not estoque:
        raise HTTPException(
            status_code=404,
            detail="Registro de estoque não encontrado"
        )

    estoque.quantidade = dados.quantidade

    db.commit()

    db.refresh(estoque)

    return estoque


# Rota para excluir um estoque por ID.
@router.delete(
    "/estoque/{idEstoque}",
    status_code=200
)
def excluir_estoque(
    idEstoque: int,
    db: Session = Depends(get_db)
):

    estoque = db.query(Estoque).filter(
        Estoque.idEstoque == idEstoque
    ).first()

    if not estoque:
        raise HTTPException(
            status_code=404,
            detail="Registro de estoque não encontrado"
        )

    db.delete(estoque)

    db.commit()

    return {
        "message": "Registro de estoque removido com sucesso"
    }