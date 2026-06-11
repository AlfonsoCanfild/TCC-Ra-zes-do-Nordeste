from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.core.dependencies import permitir_perfis
from app.core.auditoria import registrar_auditoria

from app.domain.models.pedido import Pedido
from app.domain.models.usuario import Usuario
from app.domain.models.unidade import Unidade

from app.schema.pedido_schema import (
    CanalPedidoEnum,
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
    db: Session = Depends(get_db),
    usuario_logado = Depends(
        permitir_perfis(
            ["ADMIN", "GERENTE", "CLIENTE"]
        )
    )
):

    usuario = db.query(Usuario).filter(
        Usuario.email == usuario_logado["email"]
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
        idUsuario=usuario.idUsuario,
        idUnidade=pedido.idUnidade,
        canalPedido=pedido.canalPedido,
        status="CRIADO",
        total=0
    )

    db.add(novo_pedido)

    db.commit()

    db.refresh(novo_pedido)
    
    # Registra a ação de criação do pedido na tabela de auditoria, associando-a ao usuário que realizou a ação.
    registrar_auditoria(
        db=db,
        idUsuario=usuario.idUsuario,
        acao="CRIAR",
        entidade="PEDIDO",
        idRegistro=novo_pedido.idPedido
    )

    return novo_pedido

# Rota para listar todos os pedidos, considerando a validação do usuário
@router.get(
    "/pedidos",
    response_model=list[PedidoResponse]
)
def listar_pedidos(
    db: Session = Depends(get_db),
    usuario_logado = Depends(
        permitir_perfis(
            ["ADMIN", "GERENTE"]
        )
    ),
    canalPedido: CanalPedidoEnum = None
):

    query = db.query(Pedido)

    # Se o canal for informado, filtra — senão retorna todos
    if canalPedido:
        query = query.filter(
            Pedido.canalPedido == canalPedido
        )

    return query.all()

# Rota para buscar um pedido por ID, considerando a validação do usuário
@router.get(
    "/pedidos/{idPedido}",
    response_model=PedidoResponse
)
def buscar_pedido(
    idPedido: int,
    db: Session = Depends(get_db),
    usuario_logado = Depends(
        permitir_perfis(
            ["ADMIN", "GERENTE"]
        )
    )
):

    pedido = db.query(Pedido).filter(
        Pedido.idPedido == idPedido
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    return pedido