from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

from app.domain.models.pedido import Pedido
from app.domain.models.usuario import Usuario
from app.domain.models.unidade import Unidade

from app.schema.pedido_schema import (
    PedidoCreate,
    PedidoResponse
)

router = APIRouter(tags=["Pedidos"])


# Rota para criar um novo pedido, considerando a validação do usuário e da unidade
@router.post(
    "/pedidos",
    response_model=PedidoResponse,
    status_code=201
)
def criar_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.idUsuario == pedido.idUsuario
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    unidade = db.query(Unidade).filter(
        Unidade.idUnidade == pedido.idUnidade
    ).first()

    if not unidade:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    novo_pedido = Pedido(
        idUsuario=pedido.idUsuario,
        idUnidade=pedido.idUnidade,
        canalPedido=pedido.canalPedido,
        status="CRIADO",
        total=0
    )

    db.add(novo_pedido)

    db.commit()

    db.refresh(novo_pedido)

    return novo_pedido