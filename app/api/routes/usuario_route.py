from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.domain.models.usuario import Usuario
from app.infrastructure.database.database import get_db
from app.core.security import gerar_hash
from app.core.dependencies import permitir_perfis
from app.schema.usuario_schema import (
    UsuarioCreate,
    UsuarioResponse
)

router = APIRouter(tags=["Usuários"]) # Define o prefixo para as rotas de usuário, exemplo: /usuarios

# Função para criar um novo usuário, protegida para ser acessada apenas por usuários com perfil "ADMIN"
@router.post("/usuarios", status_code=201)
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_logado = Depends(
        permitir_perfis(["ADMIN"])
    )
):

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash(usuario.senha), # Gera um hash da senha antes de armazená-la no banco de dados
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
    
# Rota para listar todos os usuários, protegida para ser acessada apenas por usuários com perfil "ADMIN"
@router.get(
    "/usuarios",
    response_model=list[UsuarioResponse] # Define o modelo de resposta para a lista de usuários, utilizando o schema UsuarioResponse
)
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario = Depends(
        permitir_perfis(
            ["ADMIN"]
        )
    )
):

    usuarios = db.query(Usuario).all()

    return usuarios