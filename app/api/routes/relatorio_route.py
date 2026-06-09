from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.infrastructure.database.database import get_db

from app.domain.models.pedido import Pedido

from app.schema.relatorio_schema import (
    RelatorioVendasResponse
)

from app.core.dependencies import permitir_perfis

router = APIRouter(tags=["Relatórios"])

# Rota para gerar relatório de vendas, acessível apenas para usuários com perfil ADMIN ou GERENTE
@router.get(
    "/relatorios/vendas",
    response_model=RelatorioVendasResponse
)
def relatorio_vendas(
    db: Session = Depends(get_db),
    usuario = Depends(
        permitir_perfis(
            ["ADMIN", "GERENTE"]
        )
    )
):

    total_vendas = db.query(
        func.sum(Pedido.total)
    ).scalar()

    quantidade_pedidos = db.query(
        Pedido
    ).count()

    return {
        "total_vendas": total_vendas or 0,
        "quantidade_pedidos": quantidade_pedidos
    }