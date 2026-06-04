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
    db: Session = Depends(get_db)
):

    pedido = db.query(Pedido).filter(
        Pedido.idPedido == item.idPedido
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    produto = db.query(Produto).filter(
        Produto.idProduto == item.idProduto
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    estoque = db.query(Estoque).filter(
        Estoque.idProduto == item.idProduto
    ).first()

    if not estoque:
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

    db.add(novo_item)

    # baixa estoque
    estoque.quantidade -= item.quantidade

    # recalcula total do pedido
    pedido.total += Decimal(produto.preco) * item.quantidade

    db.commit()

    db.refresh(novo_item)

    return novo_item