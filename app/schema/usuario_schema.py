from pydantic import BaseModel

# Esquema para criar um novo usuário
class UsuarioResponse(BaseModel):

    idUsuario: int
    nome: str
    email: str
    perfil: str

    class Config: # Configurações para o modelo Pydantic
        from_attributes = True