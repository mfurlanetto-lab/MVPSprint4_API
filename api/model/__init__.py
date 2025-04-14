from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
# importando os elementos definidos no modelo
from .base import Base

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
# Caminho absoluto para o banco de dados  
db_url = f'sqlite:///{os.path.join(os.path.dirname(__file__), "..", "database", "conversor.db")}'

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco 
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
