from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from app.infrastructure.database.database import get_db
from app.domain.models.produto import Produto
from app.schema.produto_schema import (
    ProdutoCreate,
    ProdutoResponse
)

router = APIRouter(tags=["Produtos"]) # Cria um roteador para as rotas relacionadas a produtos, com a tag "Produtos".

# Rota para criar um novo produto
@router.post(
    "/produtos",
    response_model=ProdutoResponse,
    status_code=201
)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db)
): # Define a função criar_produto que recebe um objeto do tipo ProdutoCreate e uma sessão de banco de dados como dependência.

    novo_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        status=produto.status
    )

    db.add(novo_produto)

    db.commit()

    db.refresh(novo_produto)

    return novo_produto


# Rota para listar todos os produtos
@router.get(
    "/produtos",
    response_model=list[ProdutoResponse]
)
def listar_produtos(
    db: Session = Depends(get_db)
):
    produtos = db.query(Produto).all()

    return produtos