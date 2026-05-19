from fastapi import FastAPI

from app.infrastructure.database.database import engine, Base
from app.domain.models.usuario import Usuario
from app.api.routes.usuario_route import router as usuario_router

app = FastAPI()

app.include_router(usuario_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API Raízes do Nordeste"}