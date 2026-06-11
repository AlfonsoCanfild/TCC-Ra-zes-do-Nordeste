from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    DateTime,
    Enum as SAEnum  # Enum do SQLAlchemy para o banco de dados
)

from sqlalchemy.sql import func
from app.infrastructure.database.database import Base

# Modelo de Pedido representando a tabela "pedidos" no banco de dados
class Pedido(Base):

    __tablename__ = "pedidos"

    idPedido = Column(
        Integer,
        primary_key=True,
        index=True
    )

    idUsuario = Column(
        Integer,
        ForeignKey("usuarios.idUsuario"),
        nullable=False
    )

    idUnidade = Column(
        Integer,
        ForeignKey("unidades.idUnidade"),
        nullable=False
    )

    # Enum no banco garante integridade mesmo fora da API, conforme regra de negócios
    canalPedido = Column(
        SAEnum("APP", "TOTEM", "BALCAO", "PICKUP", "WEB", name="canal_pedido_enum"),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False
    )

    total = Column(
        Numeric(10, 2),
        nullable=False
    )

    criado_em = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )