from sqlalchemy import Column, String
from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker
from .base import Base
from . import engine  


class Moeda (Base):
    __tablename__ = 'moeda'

    moeda_id = Column(String(3), primary_key=True)
    nome = Column(String(100), nullable=False)
    simbolo = Column(String(15), nullable=False)

    def __init__(self, moeda_id: str, nome: str, 
                 simbolo: str):

        self.moeda_id = moeda_id
        self.nome = nome  
        self.simbolo = simbolo


    @classmethod    
    def obter_moeda(cls, moeda_id: str):        
        Session = sessionmaker(bind=engine)        
        with Session() as session:        
           return session.query(cls).filter_by(moeda_id=moeda_id).first()
    
    @classmethod
    def existe_moeda(cls, moeda_id: str):        
        Session = sessionmaker(bind=engine)        
        with Session() as session:        
           return session.query(cls).filter_by(moeda_id=moeda_id).first() is not None

    @classmethod    
    def listar_moedas(cls):        
        Session = sessionmaker(bind=engine)        
        with Session() as session:        
           return session.query(cls).order_by(cls.moeda_id).all()
        
    def to_dict(self):        
        return {
            'moeda_id': self.moeda_id,
            'nome': self.nome       
        }    
