# API - Conversor de Moedas

Este projeto é o trabalho final para a disciplina de Arquitetura de Software do curso de Engenharia de Software. 

A API busca as cotações de moedas na plataforma ExchangeRate (https://www.exchangerate-api.com).

Foram criados dois repositórios: api e front-end.

As soluções utilizadas foram: Flask, SqlAlchemy e SQLite.

---
## Como executar

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.

Após clonar o repositório do GIT, é necessário ir ao diretório raiz do projeto, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
