from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.infrastructure.database.database import Base

# Modelo representando a tabela "pagamentos" no banco de dados
class Pagamento(Base):

    __tablename__ = "pagamentos"

    idPagamento = Column(
        Integer,
        primary_key=True,
        index=True
    )

    idPedido = Column(
        Integer,
        ForeignKey("pedidos.idPedido"),
        nullable=False
    )

    formaPagamento = Column(
        String(30),
        nullable=False
    )

    valor = Column(
        Numeric(10, 2),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False
    )

    criado_em = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )