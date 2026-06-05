from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

from app.domain.models.pagamento import Pagamento
from app.domain.models.pedido import Pedido

from app.schema.pagamento_schema import (
    PagamentoMockRequest,
    PagamentoResponse
)

router = APIRouter(tags=["Pagamentos"])


# Rota para simular um pagamento: o cliente envia uma requisição com o ID do pedido e a forma de pagamento
@router.post(
    "/pagamentos/mock",
    response_model=PagamentoResponse,
    status_code=201
)
def realizar_pagamento_mock(
    pagamento: PagamentoMockRequest,
    db: Session = Depends(get_db)
):

    pedido = db.query(Pedido).filter(
        Pedido.idPedido == pagamento.idPedido
    ).first()

    if not pedido: # Verifica se o pedido existe antes de processar o pagamento
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    if pedido.status == "PAGO": # Verifica se o pedido já foi pago para evitar pagamentos duplicados
        raise HTTPException(
            status_code=409,
            detail="Pedido já foi pago"
        )

    # Cria um novo registro de pagamento com os dados fornecidos e o valor total do pedido, e atualiza o status para "PAGO"
    novo_pagamento = Pagamento(
        idPedido=pedido.idPedido,
        formaPagamento=pagamento.formaPagamento,
        valor=pedido.total,
        status="APROVADO"
    )

    db.add(novo_pagamento)

    pedido.status = "PAGO"

    db.commit()

    db.refresh(novo_pagamento)

    return novo_pagamento