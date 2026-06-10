from sqlalchemy.orm import Session

from app.domain.models.auditoria import Auditoria

# Função para registrar uma ação de auditoria no banco de dados
def registrar_auditoria(
    db: Session,
    idUsuario: int,
    acao: str,
    entidade: str,
    idRegistro: int
):

    log = Auditoria(
        idUsuario=idUsuario,
        acao=acao,
        entidade=entidade,
        idRegistro=idRegistro
    )

    db.add(log)

    db.commit()