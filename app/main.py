from fastapi import FastAPI

from app.infrastructure.database.database import engine, Base # Importa o objeto Base do módulo de banco de dados para criar as tabelas
from app.domain.models.usuario import Usuario # Importa a classe Usuario
from app.api.routes.usuario_route import router as usuario_router # Importa o roteador de rotas do usuário
from app.api.routes.auth_route import router as auth_router # Importa o roteador de rotas de autenticação
from app.domain.models.produto import Produto # Importa a classe Produto
from app.api.routes.produto_route import router as produto_router # Importa o roteador de rotas de produto
from app.domain.models.unidade import Unidade # Importa a classe Unidade
from app.api.routes.unidade_route import router as unidade_router # Importa o roteador de rotas de unidade
from app.domain.models.estoque import Estoque # Importa a classe Estoque
from app.api.routes.estoque_route import router as estoque_router # Importa o roteador de rotas de estoque
from app.api.routes.pedido_route import router as pedido_router # Importa o roteador de rotas de pedido
from app.domain.models.item_pedido import ItemPedido # Importa a classe ItemPedido
from app.api.routes.item_pedido_route import router as item_pedido_router # Importa o roteador de rotas de item de pedido

app = FastAPI()

app.include_router(auth_router) # Inclui as rotas de autenticação
app.include_router(usuario_router) # Inclui as rotas do usuário
app.include_router(produto_router) # Inclui as rotas de produto
app.include_router(unidade_router) # Inclui as rotas de unidade
app.include_router(estoque_router) # Inclui as rotas de estoque
app.include_router(pedido_router) # Inclui as rotas de pedido
app.include_router(item_pedido_router) # Inclui as rotas de item de pedido

Base.metadata.create_all(bind=engine) # Cria as tabelas no banco de dados

# Rota raiz para verificar se a API está funcionando e para fornecer uma mensagem de boas-vindas
@app.get("/")
def root():
    return {"message": "API Raízes do Nordeste"}