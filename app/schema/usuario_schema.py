from pydantic import BaseModel, EmailStr


# Schema para criação de usuário
class UsuarioCreate(BaseModel):

    nome: str

    email: EmailStr  # Valida formato de e-mail automaticamente

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