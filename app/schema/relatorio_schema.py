from decimal import Decimal
from pydantic import BaseModel

# Esquema de resposta para o relatório de vendas
class RelatorioVendasResponse(BaseModel):

    total_vendas: Decimal

    quantidade_pedidos: int