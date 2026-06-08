from fastapi import Depends
from fastapi import HTTPException

from app.core.auth import get_current_user

# Função de dependência para verificar se o usuário tem um dos perfis permitidos
def permitir_perfis(perfis: list):

    def verificar_usuario(
        usuario = Depends(get_current_user)
    ):

        if usuario["perfil"] not in perfis:

            raise HTTPException(
                status_code=403,
                detail="Acesso negado"
            )

        return usuario

    return verificar_usuario