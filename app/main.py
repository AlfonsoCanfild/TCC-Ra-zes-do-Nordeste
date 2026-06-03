from fastapi import FastAPI

from app.infrastructure.database.database import engine, Base # Importa o objeto Base do módulo de banco de dados para criar as tabelas
from app.domain.models.usuario import Usuario # Importa a classe Usuario do módulo de modelos
from app.api.routes.usuario_route import router as usuario_router # Importa o roteador de rotas do usuário para incluir as rotas
from app.api.routes.auth_route import router as auth_router # Importa o roteador de rotas de autenticação para incluir as rotas
from app.domain.models.produto import Produto # Importa a classe Produto do módulo de modelos
from app.api.routes.produto_route import router as produto_router # Importa o roteador de rotas de produto para incluir as rotas

app = FastAPI()

app.include_router(auth_router) # Inclui as rotas de autenticação no app

app.include_router(usuario_router) # Inclui as rotas do usuário no app

app.include_router(produto_router) # Inclui as rotas de produto no app

Base.metadata.create_all(bind=engine) # Cria as tabelas no banco de dados

# Rota raiz para verificar se a API está funcionando e para fornecer uma mensagem de boas-vindas
@app.get("/")
def root():
    return {"message": "API Raízes do Nordeste"}