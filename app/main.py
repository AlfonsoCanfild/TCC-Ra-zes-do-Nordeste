from fastapi import FastAPI

from app.infrastructure.database.database import engine, Base
from app.domain.models.usuario import Usuario
from app.api.routes.usuario_route import router as usuario_router
from app.api.routes.auth_route import router as auth_router

app = FastAPI()

app.include_router(auth_router) # Inclui as rotas de autenticação no app

app.include_router(usuario_router) # Inclui as rotas do usuário no app

Base.metadata.create_all(bind=engine) # Cria as tabelas no banco de dados


@app.get("/")
def root():
    return {"message": "API Raízes do Nordeste"}