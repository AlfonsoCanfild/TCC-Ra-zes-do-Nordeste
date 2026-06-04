from decimal import Decimal
from pydantic import BaseModel

# Esquema de Pedido para criação e resposta, utilizando Pydantic para validação e serialização dos dados
class PedidoCreate(BaseModel):

    idUsuario: int

    idUnidade: int

    canalPedido: str

# Esquema de Pedido para resposta, incluindo o ID do pedido e os campos do pedido, utilizando Pydantic
class PedidoResponse(BaseModel):

    idPedido: int

    idUsuario: int

    idUnidade: int

    canalPedido: str

    status: str

    total: Decimal

    class Config:
        from_attributes = True