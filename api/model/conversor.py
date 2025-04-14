from decimal import Decimal, getcontext

class Conversao:
    def __init__(self, taxa_de: Decimal, taxa_para: Decimal, valor: Decimal):        
        self.taxa_de_para = taxa_para / taxa_de
        self.taxa_para_de = taxa_de / taxa_para
        self.valor_convertido = self.converter(valor)

    def converter(self, valor):
        # Configura o contexto para operações decimais
        getcontext().prec = 10
        valor_decimal = Decimal(valor)
        return valor_decimal * self.taxa_de_para    
        
        