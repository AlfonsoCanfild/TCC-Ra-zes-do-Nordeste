from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Biblioteca para manipulação de tokens JWT
from jose import jwt
from jose import JWTError

# Biblioteca para autenticação OAuth2
from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "raizes_do_nordeste_secret"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

tz_sp = ZoneInfo("America/Sao_Paulo")

# Configuração do esquema de autenticação OAuth2, especificando a URL para obtenção do token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# Função para criar um token JWT com os dados fornecidos e um tempo de expiração
def criar_token(data: dict):

    payload = data.copy()

    expire = datetime.now(tz_sp) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# Função para obter o usuário atual a partir do token JWT fornecido
def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")
        perfil = payload.get("perfil")

        if email is None:

            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        return {
            "idUsuario": payload.get("idUsuario"),
            "email": email,
            "perfil": perfil
        }

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )