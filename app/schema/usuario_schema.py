from pydantic import BaseModel


# Schema para criação de usuário
class UsuarioCreate(BaseModel):

    nome: str

    email: str

    senha: str

    perfil: str


# Schema para resposta
class UsuarioResponse(BaseModel):

    idUsuario: int

    nome: str

    email: str

    perfil: str

    class Config:
        from_attributes = True