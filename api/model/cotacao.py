from sqlalchemy import Column, String, DateTime, Numeric 
from datetime import datetime
from typing import Union
from decimal import Decimal, getcontext
import requests


class CotacaoUSD:
    def __init__(self, moeda_id: str, taxa: Union[Decimal, float], data_cotacao: datetime):
        self.moeda_id = moeda_id
        self.taxa = taxa # A taxa será passada
        self.data_cotacao = data_cotacao # A data será passada


    @classmethod
    def from_moeda(cls, moeda_id: str):
        taxa, data_cotacao = cls.obter_cotacaoUSD(moeda_id)
        return cls(moeda_id=moeda_id, taxa=taxa, data_cotacao = data_cotacao)

    @classmethod
    def obter_cotacaoUSD(cls, moeda_id):
        # Configura o contexto para operações decimais
        getcontext().prec = 10

        url = f"https://api.exchangerate-api.com/v4/latest/USD"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lança exceção para erros HTTP
            data = response.json()
            # Converte a taxa para Decimal
            taxa = Decimal(data["rates"][moeda_id])
            data_cotacao = datetime.strptime(data["date"], '%Y-%m-%d')  # Converte a data para datetime
            return taxa, data_cotacao
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter cotação: {e}")
            return None, None