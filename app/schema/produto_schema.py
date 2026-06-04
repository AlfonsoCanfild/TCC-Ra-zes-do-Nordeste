from pydantic import BaseModel
from decimal import Decimal

class ProdutoCreate(BaseModel): # Usada para criar um novo produto.

    nome: str

    descricao: str

    preco: Decimal

    status: str
    
# Schema de resposta

class ProdutoResponse(BaseModel): # Usada para representar a resposta de um produto, incluindo o ID do produto.

    idProduto: int

    nome: str

    descricao: str

    preco: Decimal

    status: str

    class Config:
        from_attributes = True
        
class ProdutoUpdate(BaseModel): # Classe usada para atualizar um produto existente.

    nome: str

    descricao: str

    preco: Decimal

    status: str