from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.schema.auth_schema import LoginRequest

from app.domain.models.usuario import Usuario

from app.infrastructure.database.database import get_db

from app.core.security import verificar_senha
from app.core.auth import criar_token

router = APIRouter(tags=["Auth"])


@router.post("/auth/login")
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

    if not verificar_senha(
        dados.senha,
        usuario.senha
    ):

        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

    token = criar_token({
        "sub": usuario.email,
        "perfil": usuario.perfil
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }