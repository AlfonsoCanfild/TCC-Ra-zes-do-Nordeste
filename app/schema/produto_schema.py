from pydantic import BaseModel
from decimal import Decimal

class ProdutoCreate(BaseModel): # Define a classe ProdutoCreate que herda da base

    nome: str

    descricao: str

    preco: Decimal

    status: str
    
# Schema de resposta

class ProdutoResponse(BaseModel): # Define a classe ProdutoResponse que herda da base

    idProduto: int

    nome: str

    descricao: str

    preco: Decimal

    status: str

    class Config:
        from_attributes = True