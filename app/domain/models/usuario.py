from sqlalchemy import Column, Integer, String
from app.infrastructure.database.database import Base

class Usuario(Base): # Define a classe Usuario que herda de Base, representando a tabela "usuarios" no banco de dados
    __tablename__ = "usuarios"

    idUsuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    perfil = Column(String(20), nullable=False)