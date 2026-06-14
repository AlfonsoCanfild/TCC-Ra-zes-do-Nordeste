from fastapi import APIRouter
from fastapi import Depends

from app.core.dependencies import permitir_perfis
from sqlalchemy.orm import Session
from app.infrastructure.database.database import get_db
from app.domain.models.produto import Produto
from fastapi import HTTPException
from app.core.auditoria import registrar_auditoria
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
    db: Session = Depends(get_db),
    usuario = Depends(
        permitir_perfis(
            ["ADMIN", "GERENTE"]
        )
    )
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
    
    # Registra a ação de criação do produto na tabela de auditoria, associando-a ao usuário que realizou a ação.
    registrar_auditoria(
        db=db,
        idUsuario=usuario["idUsuario"],
        acao="CRIAR",
        entidade="PRODUTO",
        idRegistro=novo_produto.idProduto
    )

    return novo_produto


# Rota para listar todos os produtos (apenas os ativos)
@router.get(
    "/produtos",
    response_model=list[ProdutoResponse]
)
def listar_produtos(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10 # Limite de 10 itens por página, conforme regra de negócios.
):
    offset = (page - 1) * limit # Calcula o deslocamento para a paginação com base no número da página.

    produtos = db.query(Produto).filter(
        Produto.status == "ATIVO"
    ).offset(offset).limit(limit).all()

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
    db: Session = Depends(get_db),
    usuario = Depends(
        permitir_perfis(
            ["ADMIN", "GERENTE"]
        )
    )
):

    produto = db.query(Produto).filter(
        Produto.idProduto == idProduto
    ).first()

    if not produto:
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

    registrar_auditoria(
        db=db,
        idUsuario=usuario["idUsuario"],
        acao="ATUALIZAR",
        entidade="PRODUTO",
        idRegistro=produto.idProduto
    )

    return produto


# Rota para deletar/inativar um produto
@router.delete(
    "/produtos/{idProduto}"
)
def excluir_produto(
    idProduto: int,
    db: Session = Depends(get_db),
    usuario = Depends(
        permitir_perfis(
            ["ADMIN"] # Permite que apenas usuários com perfil "ADMIN" acessem.
        )
    )
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
    
    # Registra a ação de exclusão do produto na tabela de auditoria, associando-a ao usuário que realizou a ação.
    registrar_auditoria(
        db=db,
        idUsuario=usuario["idUsuario"],
        acao="EXCLUIR",
        entidade="PRODUTO",
        idRegistro=idProduto
    )

    return {
        "message": "Produto inativado com sucesso"
    }