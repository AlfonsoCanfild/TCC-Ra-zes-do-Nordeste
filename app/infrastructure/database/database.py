from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carrega as variáveis definidas no arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") # Obtém a URL de conexão com o banco de dados a partir da variável de ambiente definida no .env

engine = create_engine(DATABASE_URL) # Cria a engine de conexão com o banco de dados usando a URL definida no .env

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()