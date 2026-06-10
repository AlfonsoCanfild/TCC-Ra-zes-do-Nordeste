from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.infrastructure.database.database import Base

# Modelo de Auditoria para registrar ações dos usuários no sistema
class Auditoria(Base):

    __tablename__ = "auditoria"

    idAuditoria = Column(
        Integer,
        primary_key=True,
        index=True
    )

    idUsuario = Column(
        Integer,
        ForeignKey("usuarios.idUsuario"),
        nullable=False
    )

    acao = Column(
        String(100),
        nullable=False
    )

    entidade = Column(
        String(50),
        nullable=False
    )

    idRegistro = Column(
        Integer,
        nullable=False
    )

    dataHora = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )