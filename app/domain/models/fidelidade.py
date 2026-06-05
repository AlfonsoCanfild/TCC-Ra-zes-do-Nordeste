from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.infrastructure.database.database import Base

# Modelo para representar o programa de fidelidade dos usuários
class Fidelidade(Base):

    __tablename__ = "fidelidade"

    idFidelidade = Column(
        Integer,
        primary_key=True,
        index=True
    )

    idUsuario = Column(
        Integer,
        ForeignKey("usuarios.idUsuario"),
        nullable=False,
        unique=True
    )

    pontos = Column(
        Integer,
        nullable=False,
        default=0
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