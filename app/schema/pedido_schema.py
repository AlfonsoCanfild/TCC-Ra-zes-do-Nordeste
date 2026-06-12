from decimal import Decimal
from enum import Enum
from pydantic import BaseModel

class CanalPedidoEnum(str, Enum):
    APP    = "APP"
    TOTEM  = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB    = "WEB"

# Enum com os status válidos para transição do pedido
class StatusPedidoEnum(str, Enum):
    CRIADO     = "CRIADO"
    EM_PREPARO = "EM_PREPARO"
    PRONTO     = "PRONTO"
    ENTREGUE   = "ENTREGUE"
    CANCELADO  = "CANCELADO"

# Esquema para atualização de status do pedido
class PedidoStatusUpdate(BaseModel):
    status: StatusPedidoEnum


class PedidoCreate(BaseModel):
    idUnidade: int
    canalPedido: CanalPedidoEnum

class PedidoResponse(BaseModel):
    idPedido: int
    idUsuario: int
    idUnidade: int
    canalPedido: str
    status: str
    total: Decimal

    class Config:
        from_attributes = True