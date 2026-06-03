from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schema.usuario_schema import UsuarioCreate
from app.domain.models.usuario import Usuario
from app.infrastructure.database.database import get_db

router = APIRouter(tags=["Usuários"]) # Define o prefixo para as rotas de usuário, exemplo: /usuarios


@router.post("/usuarios", status_code=201)
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
        perfil=usuario.perfil
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {
        "idUsuario": novo_usuario.idUsuario,
        "nome": novo_usuario.nome,
        "email": novo_usuario.email,
        "perfil": novo_usuario.perfil
    }