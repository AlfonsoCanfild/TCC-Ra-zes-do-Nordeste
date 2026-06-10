from pydantic import BaseModel
from datetime import datetime

# Esquema de resposta para auditoria
class AuditoriaResponse(BaseModel):

    idAuditoria: int

    idUsuario: int

    acao: str

    entidade: str

    idRegistro: int

    dataHora: datetime

    class Config:
        from_attributes = True