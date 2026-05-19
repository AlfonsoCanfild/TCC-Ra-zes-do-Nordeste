from fastapi import APIRouter
from app.schema.usuario_schema import UsuarioCreate

router = APIRouter()

@router.post("/usuarios") # Define a rota POST para criar um novo usuário, recebe um objeto do tipo UsuarioCreate.
def criar_usuario(usuario: UsuarioCreate):
    return usuario