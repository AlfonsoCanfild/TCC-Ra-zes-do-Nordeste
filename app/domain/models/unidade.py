from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.infrastructure.database.database import Base

class Unidade(Base): # Cria a classe Unidade, representando a tabela "unidades" no banco de dados.

    __tablename__ = "unidades"

    idUnidade = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        nullable=False
    )

    cidade = Column(
        String(100),
        nullable=False
    )

    estado = Column(
        String(2),
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