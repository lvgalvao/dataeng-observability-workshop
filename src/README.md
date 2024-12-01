# **Pipeline ETL com Instrumentação Automática usando OpenTelemetry**

Este projeto demonstra como criar um pipeline ETL simples com **Python**, incluindo a extração de dados de uma API, transformação usando **Pydantic**, e carregamento dos dados em um banco de dados SQLite usando **SQLAlchemy**. O projeto também apresenta como instrumentar automaticamente o código usando **OpenTelemetry** para monitoramento de métricas e traces.

---

## **Estrutura do Projeto**

### **1. Pipeline ETL Simples**
O pipeline consiste em três etapas principais:
1. **Extract**: Faz uma requisição HTTP para uma API pública e retorna os dados.
2. **Transform**: Valida e transforma os dados recebidos usando Pydantic.
3. **Load**: Insere os dados validados em um banco de dados SQLite em memória usando SQLAlchemy.

### **2. Instrumentação Automática com OpenTelemetry**
- Automatiza a coleta de métricas e traces para bibliotecas como **requests** e **SQLAlchemy**.
- Permite monitorar desempenho e comportamento do pipeline sem modificar diretamente o código.

---

## **Executando o Pipeline ETL Simples**

### **Pré-requisitos**
1. **Python 3.8 ou superior** instalado.
2. Instale as dependências:
   ```bash
   pip install requests pydantic sqlalchemy
   ```

### **Como Rodar**
Execute o código do pipeline ETL:
```bash
python pipeline.py
```

### **Explicação do Código**

#### **Extract**
A função `extract` faz uma requisição HTTP para a API do Coinbase para obter o valor do Bitcoin em dólares. Retorna os dados no formato JSON.

```python
def extract():
    response = requests.get(url="https://api.coinbase.com/v2/prices/spot?currency=USD")
    return response.json()
```

#### **Transform**
A função `transform` valida os dados retornados pela API usando o **Pydantic**. Se os dados estiverem no formato esperado, eles são transformados em um dicionário estruturado.

```python
def transform(data):
    validated_data = ApiResponse(**data)
    return validated_data.model_dump()
```

#### **Load**
A função `load` insere os dados validados em uma tabela SQLite chamada `bitcoin_data` usando o **SQLAlchemy**.

```python
def load(data):
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    bitcoin_entry = BitcoinDataModel(
        amount=data['data']['amount'],
        base=data['data']['base'],
        currency=data['data']['currency']
    )

    session.add(bitcoin_entry)
    session.commit()

    results = session.query(BitcoinDataModel).all()
    print("Dados armazenados no SQLite (via SQLAlchemy):")
    for result in results:
        print(f"Amount: {result.amount}, Base: {result.base}, Currency: {result.currency}")

    session.close()
```

---

## **Instrumentação Automática com OpenTelemetry**

A instrumentação automática usa o **OpenTelemetry** para capturar métricas e traces sem modificar o código do pipeline. Bibliotecas como **requests** e **SQLAlchemy** são automaticamente instrumentadas para coletar dados de monitoramento.

### **Pré-requisitos**
1. Instale as dependências do OpenTelemetry:
   ```bash
   pip install opentelemetry-distro opentelemetry-instrumentation-requests opentelemetry-instrumentation-sqlalchemy
   ```

2. Configure o nome do serviço e o exportador:
   ```bash
   export OTEL_RESOURCE_ATTRIBUTES="service.name=pipeline_etl"
   export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
   ```

### **Como Rodar**
Execute o pipeline com o comando de instrumentação automática:
```bash
opentelemetry-instrument --traces_exporter console --metrics_exporter none python pipeline.py
```

---

## **O Que Será Monitorado**

### **Requisições HTTP**
Traces capturam informações como:
- Método HTTP (`GET`).
- URL da API.
- Código de status da resposta.

Exemplo:
```json
{
    "name": "GET",
    "attributes": {
        "http.method": "GET",
        "http.url": "https://api.coinbase.com/v2/prices/spot?currency=USD",
        "http.status_code": 200
    }
}
```

### **Operações SQL**
Traces capturam detalhes das operações SQL, como:
- Sistema de banco de dados (`sqlite`).
- Comandos SQL executados (`INSERT`, `SELECT`).
- Duração de cada operação.

Exemplo:
```json
{
    "name": "INSERT",
    "attributes": {
        "db.system": "sqlite",
        "db.statement": "INSERT INTO bitcoin_data (amount, base, currency) VALUES (?, ?, ?)"
    }
}
```

---

## **Dicas de Monitoramento**

### **Visualização no Console**
Ao rodar com `--traces_exporter console`, todos os traces serão exibidos diretamente no terminal.

### **Integração com Ferramentas de Observabilidade**
Para visualizar métricas e traces em ferramentas como **Grafana Tempo** ou **Jaeger**, configure o OpenTelemetry com os exportadores apropriados:
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
opentelemetry-instrument --traces_exporter otlp --metrics_exporter none python pipeline.py
```

---

## **Contribuição**

Sinta-se à vontade para abrir **issues** ou enviar **pull requests** caso encontre problemas ou deseje melhorar este projeto.

---

## **Licença**

Este projeto está licenciado sob a MIT License. Consulte o arquivo `LICENSE` para mais informações.