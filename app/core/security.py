from passlib.context import CryptContext # Importa a classe CryptContext da biblioteca passlib para lidar com o hashing de senhas

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def gerar_hash(senha: str): # Gerar um hash da senha usando a biblioteca bcrypt
    return pwd_context.hash(senha)

def verificar_senha(
    senha_plana: str,
    senha_hash: str
):
    return pwd_context.verify(
        senha_plana,
        senha_hash
    )