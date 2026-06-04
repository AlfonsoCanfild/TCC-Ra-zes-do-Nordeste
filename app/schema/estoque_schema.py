from pydantic import BaseModel

# Esquemas para o modelo de Estoque.
class EstoqueCreate(BaseModel):

    idUnidade: int

    idProduto: int

    quantidade: int

# Esquema para atualização do estoque, permitindo apenas a atualização da quantidade.
class EstoqueUpdate(BaseModel):

    quantidade: int

# Esquema de resposta para o estoque, incluindo o ID do estoque e os IDs relacionados de unidade e produto.
class EstoqueResponse(BaseModel):

    idEstoque: int

    idUnidade: int

    idProduto: int

    quantidade: int

    class Config:
        from_attributes = True