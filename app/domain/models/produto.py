from sqlalchemy import Column, Integer, String, Numeric

from app.infrastructure.database.database import Base

class Produto(Base): # Define a classe Produto que vai herdar de Base, representando a tabela "produtos" no banco de dados
    __tablename__ = "produtos"

    idProduto = Column(Integer, primary_key=True, index=True)

    nome = Column(String(50), nullable=False)

    descricao = Column(String(100), nullable=True)

    preco = Column(Numeric(10, 2), nullable=False)

    status = Column(String(20), nullable=False)