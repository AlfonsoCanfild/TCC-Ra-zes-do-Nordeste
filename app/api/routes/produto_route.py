from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from app.infrastructure.database.database import get_db
from app.domain.models.produto import Produto
from fastapi import HTTPException
from app.schema.produto_schema import (
    ProdutoCreate,
    ProdutoResponse,
    ProdutoUpdate
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


# Rota para listar todos os produtos (apenas os ativos)
@router.get(
    "/produtos",
    response_model=list[ProdutoResponse]
)
def listar_produtos(
    db: Session = Depends(get_db)
):
    produtos = db.query(Produto).filter(
        Produto.status == "ATIVO"
    ).all()

    return produtos


# Rota para buscar um produto por ID
@router.get(
    "/produtos/{idProduto}",
    response_model=ProdutoResponse
)
def buscar_produto(
    idProduto: int,
    db: Session = Depends(get_db)
):
    produto = db.query(Produto).filter(
        Produto.idProduto == idProduto
    ).first()

    if not produto:# Lança uma exceção HTTP 404 se o produto não for encontrado.
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return produto


# Rota para atualizar um produto
@router.put(
    "/produtos/{idProduto}",
    response_model=ProdutoResponse
)
def atualizar_produto(
    idProduto: int,
    dados: ProdutoUpdate,
    db: Session = Depends(get_db)
):

    produto = db.query(Produto).filter(
        Produto.idProduto == idProduto
    ).first()

    if not produto: # Lança uma exceção HTTP 404 se o produto não for encontrado no banco de dados.
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    produto.nome = dados.nome
    produto.descricao = dados.descricao
    produto.preco = dados.preco
    produto.status = dados.status

    db.commit()

    db.refresh(produto)

    return produto


# Rota para deletar/inativar um produto
@router.delete(
    "/produtos/{idProduto}",
    status_code=200
)
def inativar_produto(
    idProduto: int,
    db: Session = Depends(get_db)
):

    produto = db.query(Produto).filter(
        Produto.idProduto == idProduto
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    produto.status = "INATIVO"

    db.commit()

    return {
        "message": "Produto inativado com sucesso"
    }