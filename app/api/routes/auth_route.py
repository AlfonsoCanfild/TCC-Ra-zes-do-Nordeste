from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm # Importa o formulário de requisição de login do FastAPI

from app.domain.models.usuario import Usuario

from app.infrastructure.database.database import get_db

from app.core.security import verificar_senha
from app.core.auth import criar_token

router = APIRouter(tags=["Auth"])

# Rota de login para autenticação do usuário e geração de token JWT
@router.post("/auth/login")
def login(
    dados: OAuth2PasswordRequestForm = Depends(), # Recebe os dados de login (username e password)
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.email == dados.username
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

    senha_valida = verificar_senha(
        dados.password,
        usuario.senha
    )

    if not senha_valida:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

    token = criar_token({
        "sub": usuario.email,
        "perfil": usuario.perfil,
        "idUsuario": usuario.idUsuario
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }