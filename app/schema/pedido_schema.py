from decimal import Decimal
from enum import Enum
from pydantic import BaseModel

# Apenas os canais válidos conforme regra de negócio
class CanalPedidoEnum(str, Enum):
    APP    = "APP"
    TOTEM  = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB    = "WEB"

# Esquema de Pedido para criação e resposta
class PedidoCreate(BaseModel):

    idUnidade: int

    canalPedido: CanalPedidoEnum  # Pydantic valida e rejeita valores inválidos com 422

# Esquema de Pedido para resposta
class PedidoResponse(BaseModel):

    idPedido: int

    idUsuario: int

    idUnidade: int

    canalPedido: str

    status: str

    total: Decimal

    class Config:
        from_attributes = True