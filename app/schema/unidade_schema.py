from pydantic import BaseModel

# Esquemas para a entidade Unidade, definindo as classes de criação, atualização e resposta.
class UnidadeCreate(BaseModel):

    nome: str

    cidade: str

    estado: str

    status: str

# Esquema para atualização de Unidade.
class UnidadeUpdate(BaseModel):

    nome: str

    cidade: str

    estado: str

    status: str

# Esquema para resposta de Unidade, incluindo o ID da unidade e configurando a classe para permitir a criação a partir de objetos ORM.
class UnidadeResponse(BaseModel):

    idUnidade: int

    nome: str

    cidade: str

    estado: str

    status: str

    class Config:
        from_attributes = True