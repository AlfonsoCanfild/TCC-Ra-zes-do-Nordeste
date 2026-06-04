from decimal import Decimal
from pydantic import BaseModel

# Esquema de ItemPedido para criação, utilizando Pydantic para validação e serialização dos dados
class ItemPedidoCreate(BaseModel):

    idPedido: int

    idProduto: int

    quantidade: int

# Esquema de ItemPedido para resposta, incluindo o ID do item pedido e os campos do item pedido
class ItemPedidoResponse(BaseModel):

    idItemPedido: int

    idPedido: int

    idProduto: int

    quantidade: int

    preco_unitario: Decimal

    class Config:
        from_attributes = True