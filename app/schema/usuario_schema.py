from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel): # Define o modelo de dados para criar um usuário
    nome: str
    email: EmailStr
    senha: str
    perfil: str