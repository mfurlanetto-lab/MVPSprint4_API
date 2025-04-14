from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, relationship
from .base import Base
from .moeda import Moeda
from . import engine  


class MoedaPreferencia (Base):
    __tablename__ = 'moeda_preferencia'

    moeda_id = Column(String(3), ForeignKey('moeda.moeda_id'), primary_key=True)
    ordem = Column(Integer, nullable=False)
    moeda = relationship("Moeda")
    
    def __init__(self, moeda_id: str, ordem : Integer):
        self.moeda_id = moeda_id
        self.ordem = ordem  

    @classmethod 
    def remover_preferencias(cls, ordens: list):  
            
        Session = sessionmaker(bind=engine)
        session = Session()   
        try:    
            for item in ordens:
                moeda_id = item.get('moeda_id')
                preferencia = session.query(cls).filter_by(moeda_id=moeda_id).first()
                if preferencia:
                    session.delete(preferencia)            
                    session.commit()            
                    return True, "Sucesso"
                else:
                    print(f"Preferência para moeda_id {moeda_id} não encontrada.")
                    return False, f"Erro ao gravar preferências. Tente novamente mais tarde."
        except Exception as e:        
            print(f"Ocorreu um erro: {e}")  
            session.rollback()      
            return False, f"Erro ao gravar preferências. Tente novamente mais tarde."   
        finally:        
            session.close()  

    @classmethod 
    def alterar_preferencias(cls, ordens: list):
    
        Session = sessionmaker(bind=engine)
        session = Session() 
        try:
            for item in ordens:
                moeda_id = item.get('moeda_id')
                nova_ordem = item.get('ordem')
                preferencia = session.query(cls).filter_by(moeda_id=moeda_id).first()
                if preferencia:
                    preferencia.ordem = nova_ordem
                    session.commit()
                    return True, "Sucesso"
                else:
                    print(f"Preferência para moeda_id {moeda_id} não encontrada.")
                    return False, f"Erro ao gravar preferências. Tente novamente mais tarde."
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            session.rollback()
            return False, f"Erro ao gravar preferências. Tente novamente mais tarde."
        finally:        
            session.close()  

    @classmethod 
    def incluir_preferencias(cls, nova: list):  

        Session = sessionmaker(bind=engine)
        session = Session() 
        try: 
            for item in nova:
                moeda_id = item.get('moeda_id')
                ordem = item.get('ordem')
                nova_preferencia = cls(moeda_id=moeda_id, ordem=ordem)            
                session.add(nova_preferencia)  
            session.commit()
            return True, "Sucesso"
        except IntegrityError as e:
            print(f"Erro de integridade: {e}")  # Loga o erro no console
            session.rollback()
            return False, f"Erro ao gravar preferências. Tente novamente mais tarde."
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            session.rollback()
            return False, f"Erro ao gravar preferências. Tente novamente mais tarde."
        finally:        
            session.close()  

    @classmethod    
    def listar_preferencias(cls):       
        Session = sessionmaker(bind=engine)
        session = Session() 
        preferencias = session.query(cls).join(Moeda).order_by(cls.ordem).all()        
        resultado = []        
        for preferencia in preferencias:            
            resultado.append({                
                'moeda_id': preferencia.moeda_id,                
                'ordem': preferencia.ordem,                
                'nome': preferencia.moeda.nome           
            })        
        return resultado

    def to_dict(self):        
        return {
            'moeda_id': self.moeda_id,
            'ordem': self.ordem,
            'nome' : self.moeda.nome       
        }    
