from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Mykey = "1234" # senha do PostgreSQL
DATABASE_URL = "postgresql://postgres:"+Mykey+"@localhost:5432/raizes_do_nordeste"

engine = create_engine(DATABASE_URL) # cria a engine de conexão com o banco de dados

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()