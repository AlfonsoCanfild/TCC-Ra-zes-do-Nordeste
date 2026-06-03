from pydantic import BaseModel

class LoginRequest(BaseModel): # Define um modelo de dados para a requisição de login (email e senha)
    email: str
    senha: str