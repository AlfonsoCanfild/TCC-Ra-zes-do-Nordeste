from pydantic import BaseModel

class UsuarioCreate(BaseModel): # Define a classe UsuarioCreate que herda de BaseModel, são os dados necessários para criar um usuário
    nome: str
    email: str
    senha: str
    perfil: str