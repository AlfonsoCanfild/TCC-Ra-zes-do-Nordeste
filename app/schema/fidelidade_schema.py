from pydantic import BaseModel

# Esquema de resposta para o programa de fidelidade dos usuários
class FidelidadeResponse(BaseModel):

    idFidelidade: int

    idUsuario: int

    pontos: int

    class Config:
        from_attributes = True