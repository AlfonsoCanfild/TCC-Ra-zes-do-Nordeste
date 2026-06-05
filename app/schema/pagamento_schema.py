from decimal import Decimal
from pydantic import BaseModel


# Modelos de dados para requisições e respostas relacionadas a pagamentos
class PagamentoMockRequest(BaseModel):

    idPedido: int

    formaPagamento: str


# Modelo de resposta para informações de pagamento
# incluindo o ID do pagamento, ID do pedido, forma de pagamento, valor e status
class PagamentoResponse(BaseModel):

    idPagamento: int

    idPedido: int

    formaPagamento: str

    valor: Decimal

    status: str

    class Config:
        from_attributes = True