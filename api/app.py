from flask import Flask, request, render_template, jsonify
from .model.cotacao import CotacaoUSD
from .model.conversor import Conversao
from .model.moeda import Moeda
from .model.preferencia import MoedaPreferencia
from decimal import Decimal
import os   

# Obtendo o caminho absoluto para o diretório front_end   
base_dir = os.path.dirname(os.path.abspath(__file__)) 
front_end_dir = os.path.join(base_dir, '..', 'front_end')   

app = Flask(__name__, 
            static_folder=os.path.join(front_end_dir, 'static'),
            template_folder=os.path.join(front_end_dir, 'templates'))

app.debug = True  # modo de depuração
app.config['ENV'] = 'development' # ambiente de desenvolvimento

@app.route('/')
def home():
    converter_de = Moeda.listar_moedas()  # Lista de moedas
    converter_para = Moeda.listar_moedas()  # Lista de moedas   

    return render_template('index.html', converterDe=converter_de, converterPara=converter_para), 200


@app.route("/converter", methods=['POST'])
def converter():

    # Recebe a solicitação
    dados = request.get_json()  

    # Verifica se os dados foram recebidos corretamente    
    if not dados:
        jsonify({'erro': 'Dados não foram recebidos'}), 400       

    resultados = []

    # Processa cada conversão de moeda 
    for moeda in dados:        
        input_moeda_de = moeda.get('moeda_de')        
        input_moeda_para = moeda.get('moeda_para')        
        input_valor = moeda.get('valor')

        #print(f"Requisição recebida para conversão: {input_valor} {input_moeda_de} para {input_moeda_para}")

        # Verifica se valor foi fornecido
        if not input_valor:
            jsonify({'erro': 'Valor a converter não fornecido'}), 400 

        if Decimal(input_valor) <=0 :
            jsonify({'erro': 'Valor a converter deve ser maior ou igual à zero'}), 400

        # Verifica se moeda_de foi fornecida
        if not input_moeda_de:
            jsonify({'erro': 'A moeda origem não foi fornecida'}), 400

        # Verifica se moeda_para foi fornecida
        if not input_moeda_para:
           jsonify({'erro': 'A moeda destino não foi fornecida'}), 400
    
        # Verifica se moeda_de é válida
        if not Moeda.existe_moeda(input_moeda_de):
            error_msg = f"A moeda {input_moeda_de} não existe"
            jsonify({'erro': error_msg}), 400
    
        # Verifica se moeda_para é válida
        if not Moeda.existe_moeda(input_moeda_para):
            error_msg = f"A moeda {input_moeda_para} não existe"
            jsonify({'erro': error_msg}), 400
   
        moeda_de = Moeda.obter_moeda(input_moeda_de)  
        moeda_para = Moeda.obter_moeda(input_moeda_para) 

        cotacao_de = CotacaoUSD.from_moeda(moeda_de.moeda_id)  
        cotacao_para = CotacaoUSD.from_moeda(moeda_para.moeda_id)

        # Cria o objeto Conversao com as taxas, gerando o valor convertido
        conversor = Conversao(cotacao_de.taxa, cotacao_para.taxa, Decimal(input_valor))  

        valor_convertido = conversor.valor_convertido 

        if valor_convertido is not None:          
            resultados.append({                
                'valor': input_valor,                 
                'moeda_de': input_moeda_de,                
                'moeda_para': input_moeda_para,                
                'valor_convertido': valor_convertido            
                })       
        else:  
            error_msg = f'Erro na conversão de {moeda_de} para {moeda_para}'
            jsonify({'erro': error_msg}), 400

    return jsonify(resultados), 200

@app.route('/api/moedas')
def get_moedas():        
    moedas = Moeda.listar_moedas() 
    # Converter a lista de objetos em uma lista de dicionários    
    return jsonify([moeda.to_dict() for moeda in moedas]) 

@app.route('/api/preferencias')
def get_preferencias():        
    preferencias = MoedaPreferencia.listar_preferencias() 
    # Converter a lista de objetos em uma lista de dicionários    
    return jsonify(preferencias)  


def validar_dados(dados):

    # Valida as moedas e ordens recebidas 

    for item in dados:
        input_moeda_id = item.get('moeda_id') 
        input_ordem = item.get('ordem') 

        # Verifica se moeda_de foi fornecida
        if not input_moeda_id:
            return False, 'A moeda não foi fornecida'

        # Verifica se ordem foi fornecida
        if not input_ordem:
            return False, f"A ordem da moeda {input_moeda_id} não foi fornecida"
        
        # Verifica se moeda_id existe no cadastro de moedas
        if not Moeda.existe_moeda(input_moeda_id):
            return False, f"A moeda {input_moeda_id} não existe"

        # Verifica se ordem é valida
        if not isinstance(input_ordem, int):                
            return False, f"A ordem para moeda_id {input_moeda_id} não é um número inteiro."

        # Verifica se ordem é maior do que zero
        if input_ordem < 0:                
            return False, f"A ordem para moeda_id {input_moeda_id} não é maior ou igual à zero"

        return True, 'Sucesso'

@app.route('/api/removerpreferencias', methods=['DELETE'])
def remover_preferencias():
    # Recebe a solicitação
    dados = request.get_json() 

    print('DADOS EXCLUSÃO:')
    print(dados)       

    # Verifica se os dados foram recebidos corretamente    
    if not dados:
        return jsonify({'erro': 'Dados de remoção não foram recebidos'}), 400       

    if not isinstance(dados, list): 
        return jsonify({'erro': 'Dados de exclusão não estão no formato válido'}), 400  

    sucesso, mensagem = validar_dados(dados)
    if not sucesso: 
        return jsonify({'mensagem': mensagem}), 400  

    # Remove as preferências
    sucesso, mensagem = MoedaPreferencia.remover_preferencias(dados)

    if sucesso:        
        return jsonify({"mensagem": "Preferências removidas com sucesso"}), 200  
    else:        
        return jsonify({"mensagem": mensagem}), 400      


@app.route('/api/alterarpreferencias', methods=['PUT'])
def alterar_preferencias():
    # Recebe a solicitação
    dados = request.get_json()

    print('DADOS ALTERAÇÃO:')
    print(dados)   

    # Verifica se os dados foram recebidos corretamente    
    if not dados:
        return jsonify({'erro': 'Dados de alteração não foram recebidos'}), 400 
 
    if not isinstance(dados, list): 
        return jsonify({'erro': 'Dados de alteração não estão no formato válido'}), 400     

    sucesso, mensagem = validar_dados(dados)
    if not sucesso: 
        return jsonify({'mensagem': mensagem}), 400  

    # Remove as preferências
    sucesso, mensagem = MoedaPreferencia.alterar_preferencias(dados)

    if sucesso:        
        return jsonify({"mensagem": "Preferências alteradas com sucesso"}), 200  
    else:        
        return jsonify({"mensagem": mensagem}), 400      

@app.route("/api/incluirpreferencias", methods=['POST'])
def incluir_preferencias():

    # Recebe a solicitação
    dados = request.get_json()  

    # Verifica se os dados foram recebidos corretamente    
    if not dados:
        return jsonify({'erro': 'Dados de inclusão não foram recebidos'}), 400

    if not isinstance(dados, list):            
        return jsonify({'erro': 'Dados de inclusão não estão no formato válido'}), 400       

    # Valida as moedas e ordens recebidas
    sucesso, mensagem = validar_dados(dados)
    if not sucesso: 
        return jsonify({'mensagem': mensagem}), 400  

    # Inclui as preferências
    sucesso, mensagem = MoedaPreferencia.incluir_preferencias(dados)

    if sucesso:        
        return jsonify({"mensagem": "Preferências incuídas com sucesso"}), 200  
    else:        
        return jsonify({"mensagem": mensagem}), 400  

    