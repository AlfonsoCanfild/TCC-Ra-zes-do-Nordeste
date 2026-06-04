from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime
)
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base


class Estoque(Base): # Define a classe Estoque e representando a tabela de "estoque" no banco de dados.

    __tablename__ = "estoque"

    idEstoque = Column(
        Integer,
        primary_key=True,
        index=True
    )

    idUnidade = Column(
        Integer,
        ForeignKey("unidades.idUnidade"),
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

    criado_em = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    atualizado_em = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )