from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from decimal import Decimal

from app.infrastructure.database.database import get_db

from app.domain.models.item_pedido import ItemPedido
from app.domain.models.pedido import Pedido
from app.domain.models.produto import Produto
from app.domain.models.estoque import Estoque

from app.core.dependencies import permitir_perfis

from app.schema.item_pedido_schema import (
    ItemPedidoCreate,
    ItemPedidoResponse
)

router = APIRouter(tags=["Itens Pedido"])


# Rota para criar um novo item de pedido, considerando a validação do pedido e do produto
@router.post(
    "/itens-pedido",
    response_model=ItemPedidoResponse,
    status_code=201
)
def criar_item_pedido(
    item: ItemPedidoCreate,
    db: Session = Depends(get_db),
    usuario_logado = Depends(
        permitir_perfis(
            ["ADMIN", "GERENTE", "CLIENTE"]
        )
    )
):

    if item.quantidade <= 0: # Valida se a quantidade é maior que zero
        raise HTTPException(
            status_code=400,
            detail="Quantidade deve ser maior que zero"
        )

    pedido = db.query(Pedido).filter(
        Pedido.idPedido == item.idPedido
    ).first()

    if not pedido: # Valida se o pedido existe
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    produto = db.query(Produto).filter(
        Produto.idProduto == item.idProduto
    ).first()

    if not produto: #
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    estoque = db.query(Estoque).filter(
        Estoque.idProduto == item.idProduto,
        Estoque.idUnidade == pedido.idUnidade
    ).first()

    if not estoque: # Valida se o produto tem registro de estoque
        raise HTTPException(
            status_code=404,
            detail="Produto sem registro de estoque"
        )

    if estoque.quantidade < item.quantidade:
        raise HTTPException(
            status_code=409,
            detail="Estoque insuficiente"
        )

    novo_item = ItemPedido(
        idPedido=item.idPedido,
        idProduto=item.idProduto,
        quantidade=item.quantidade,
        preco_unitario=produto.preco
    )

    db.add(novo_item) # Adiciona o novo item de pedido à sessão do banco de dados

    # baixa estoque
    estoque.quantidade -= item.quantidade

    # recalcula total do pedido
    valor_item = produto.preco * Decimal(item.quantidade)

    pedido.total += valor_item

    db.commit()

    db.refresh(novo_item)

    return novo_item

# Rota para listar os itens de um pedido específico, considerando a validação do pedido
@router.get(
    "/itens-pedido/{idPedido}",
    response_model=list[ItemPedidoResponse]
)
def listar_itens_pedido(
    idPedido: int,
    db: Session = Depends(get_db),
    _ = Depends(
        permitir_perfis(["ADMIN", "GERENTE", "CLIENTE"])
    )
):

    pedido = db.query(Pedido).filter(
        Pedido.idPedido == idPedido
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    itens = db.query(ItemPedido).filter(
        ItemPedido.idPedido == idPedido
    ).all()

    return itens