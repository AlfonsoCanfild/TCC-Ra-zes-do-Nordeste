from sqlalchemy import Column, Integer, String
from app.infrastructure.database.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    idUsuario = Column(Integer, primary_key=True, index=True) # Define a coluna idUsuario como chave primária e índice
    nome = Column(String(100), nullable=False) # Define a coluna nome como string de até 100 caracteres e não nula
    email = Column(String(100), unique=True, nullable=False) # Define a coluna e-mail como string de até 100 caracteres
    senha = Column(String(255), nullable=False) # Define a coluna senha como string de até 255 caracteres e não nula
    perfil = Column(String(20), nullable=False) # Define a coluna perfil como string de até 20 caracteres e não nula