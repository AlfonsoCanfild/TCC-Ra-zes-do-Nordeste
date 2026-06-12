from pydantic import BaseModel

# Modelo criado para representar a estrutura dos dados de login, contendo os campos de email e senha,
# mas substituido pelo OAuth2PasswordRequestForm

class LoginRequest(BaseModel): # Define um modelo de dados para a requisição de login
    email: str
    senha: str