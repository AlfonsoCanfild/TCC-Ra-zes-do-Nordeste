from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    DateTime
)

from sqlalchemy.sql import func
from app.infrastructure.database.database import Base

# Cria a tabela "itens_pedido" no banco de dados, com relacionamentos para Pedido e Produto
class ItemPedido(Base):

    __tablename__ = "itens_pedido"

    idItemPedido = Column(
        Integer,
        primary_key=True,
        index=True
    )

    idPedido = Column(
        Integer,
        ForeignKey("pedidos.idPedido"),
        nullable=False
    )

    idProduto = Column(
        Integer,
        ForeignKey("produtos.idProduto"),
        nullable=False
    )

    quantidade = Column(
        Integer,
        nullable=False
    )

    preco_unitario = Column(
        Numeric(10, 2),
        nullable=False
    )

    criado_em = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    atualizado_em = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )