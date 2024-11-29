# Observabilidade ETL - Pipeline Completo

<p align="center">
  <a href="https://suajornadadedados.com.br/"><img src="https://github.com/lvgalvao/data-engineering-roadmap/raw/main/pics/logo.png" alt="Jornada de Dados"></a>
</p>
<p align="center">
    <em>Nossa missão é fornecer o melhor ensino em engenharia de dados</em>
</p>

Bem-vindo a **Jornada de Dados**

## Projeto de Observabilidade: ETL Completa para Conversão de CSV em Parquet

## Objetivo

Esse workshop faz parte da Jornada de Dados e tem como objetivo mostrar como implementar observabilidade em uma pipeline ETL completa.

## Tópicos

O workshop é separado em 4 etapas:
- Introdução e Contextualização
- Introdução ao OpenTelemetry
- Projeto Logfire, implementação de logs, métricas e traces
- Gestão de Erros e Exceções, Projeto Prometheus

### Agenda detalhada
9:00 - 9:30 - Apresentação e Contextualização
9:30 - 10:30 - Introdução ao OpenTelemetry
10:30 - 12:30 - Projeto Logfire, implementação de logs, métricas e traces
12:30 - 13:30 - Pausa para o almoço
13:30 - 16:00 - Gestão de Erros e Exceções, Projeto Prometheus

## Escalidraw

[Link](https://link.excalidraw.com/l/8pvW6zbNUnD/8YMdUcpuF1M)

## Contexto

## Open Telemetry

O **OpenTelemetry** é um framework de código aberto voltado para a observabilidade de aplicações modernas. Ele permite coletar, processar e exportar dados de telemetria como rastreamentos (traces), métricas e logs estruturados de maneira padronizada. Para engenheiros de dados que trabalham com **ETL**, **APIs** e pipelines, o OpenTelemetry oferece ferramentas poderosas para monitorar e diagnosticar problemas de performance e integridade em aplicações que utilizam tecnologias amplamente adotadas, como:

- **SQLAlchemy**: Para rastrear consultas SQL e identificar gargalos em bancos de dados.
- **FastAPI**: Para monitorar o desempenho de APIs e fluxos de requisições.
- **Boto3 (Amazon Web Services)**: Para entender a latência e os erros de chamadas a serviços AWS, como S3 e DynamoDB.
- **Requests**: Para medir tempos de resposta e rastrear chamadas a APIs externas.

---

### **Por que usar OpenTelemetry em ETLs e Pipelines de Dados?**

Em aplicações de ETL e pipelines, a observabilidade é essencial para:

- **Diagnóstico de falhas**: Identificar por que uma transformação de dados falhou ou um pipeline ficou lento.
- **Medição de desempenho**: Monitorar tempos de execução de etapas específicas, como consultas SQL ou chamadas de APIs.
- **Detecção de erros intermitentes**: Acompanhar interações entre serviços em pipelines distribuídos.

Com o OpenTelemetry, você pode instrumentar aplicações de forma automática ou manual para capturar dados críticos, como a duração de funções, número de erros e padrões de uso, tudo isso com suporte a exportação para sistemas como Prometheus, Grafana e outros.

### Começando

Vamos fazer o nosso primeiro exemplo com OpenTelemetry.

Essa aplicação usa um projeto básico usando o Streamlit para rolar um dado.

```
pip install streamlit
```

Criar e lançar nossa aplicação

```python
import streamlit as st
import logging
from random import randint

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para simular o lançamento de um dado
def roll():
    return randint(1, 6)

# Interface Streamlit
st.title("Aplicação com Streamlit e Observabilidade")
player = st.text_input("Digite o nome do jogador (opcional):")

# Lógica para lançar o dado
if st.button("Rolar o Dado"):
    result = roll()
    if player:
        logger.warning("%s está rolando o dado: %s", player, result)
        st.write(f"{player} rolou o dado e obteve: {result}")
    else:
        logger.warning("Jogador anônimo está rolando o dado: %s", result)
        st.write(f"Jogador anônimo rolou o dado e obteve: {result}")
```

rodando

```
streamlit run exemplo_01.py
```

Agora vamos instrumentar nossa aplicação.

### Instrumentação

#### **Instrumentação Zero-Code**
A **instrumentação zero-code** gera dados de telemetria automaticamente para sua aplicação, sem que você precise modificar o código. Existem várias opções para configurar esse tipo de instrumentação. Aqui, utilizaremos o agente `opentelemetry-instrument`.

---

### **Instalação**

Instale o pacote `opentelemetry-distro`, que contém a API, o SDK do OpenTelemetry e as ferramentas necessárias, como `opentelemetry-bootstrap` e `opentelemetry-instrument`.

```bash
pip install opentelemetry-distro
```

---

### **Configurar a instrumentação automática**

Execute o comando `opentelemetry-bootstrap` para instalar as dependências de instrumentação automaticamente detectadas:

```bash
opentelemetry-bootstrap -a install
```

Isso instalará instrumentações adequadas para as bibliotecas usadas em sua aplicação, como **Streamlit**, **Requests**, entre outras.

---

### **Executar a Aplicação Instrumentada**

Agora, você pode executar sua aplicação com o agente `opentelemetry-instrument`. O exemplo abaixo mostrará como ativar os exportadores de rastreamentos (traces), métricas e logs para serem exibidos no console:

```bash
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name dice-app \
    streamlit run app.py
```

### Adicionando Instrumentação Manual à Instrumentação Automática no Streamlit

A instrumentação automática captura dados de telemetria apenas nas bordas do sistema, como requisições HTTP de entrada e saída. No entanto, ela não monitora o que acontece dentro da aplicação. Para isso, precisamos adicionar **instrumentação manual**. Aqui está como vincular spans manuais aos spans gerados automaticamente.

---

### **Adicionando Rastreamentos (Traces) no Streamlit**

1. **Atualize o arquivo `app.py` para incluir a instrumentação manual:**

```python
from random import randint
import streamlit as st
from opentelemetry import trace

# Configurando o tracer
tracer = trace.get_tracer("streamlit.diceroller")

# Função para lançar um dado
def roll():
    # Criação de um novo span manual
    with tracer.start_as_current_span("roll_dice") as roll_span:
        result = randint(1, 6)
        # Adicionando atributos ao span
        roll_span.set_attribute("roll.value", result)
        return result

# Interface do Streamlit
st.title("Instrumentação Manual com OpenTelemetry")
player = st.text_input("Digite o nome do jogador (opcional):")

if st.button("Rolar o Dado"):
    with tracer.start_as_current_span("player_action") as player_span:
        result = roll()
        player_span.set_attribute("player.name", player or "Anônimo")
        st.write(f"Resultado do dado: {result}")
```

---

### **Executar a Aplicação**

Para rodar a aplicação com instrumentação manual e automática:

```bash
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name dice-app \
    streamlit run app.py
```

---

### **Testar a Instrumentação**

1. Acesse a aplicação em **http://localhost:8501**.
2. Insira o nome do jogador (opcional) e clique em "Rolar o Dado".
3. Observe o resultado no console, onde será possível ver os spans gerados.

---

### **Saída Esperada no Console**

**Span gerado automaticamente para a requisição do Streamlit**:
```json
{
    "name": "streamlit request",
    "context": {
        "trace_id": "0xdb1fc322141e64eb84f5bd8a8b1c6d1f",
        "span_id": "0x5c2b0f851030d17d"
    },
    "attributes": {
        "http.method": "GET",
        "http.route": "/",
        "service.name": "dice-app"
    }
}
```

**Span manual criado para a função `roll`**:
```json
{
    "name": "roll_dice",
    "context": {
        "trace_id": "0xdb1fc322141e64eb84f5bd8a8b1c6d1f",
        "span_id": "0x8c2b0f851230d123",
        "parent_id": "0x5c2b0f851030d17d"
    },
    "attributes": {
        "roll.value": 4
    }
}
```

**Relacionamento entre spans**:
- O span `roll_dice` é filho do span gerado automaticamente para a requisição, identificável pelo mesmo `trace_id`.

---

### **Conclusão**

Agora, sua aplicação Streamlit captura rastreamentos detalhados, incluindo spans manuais vinculados a spans automáticos. Isso permite monitorar partes específicas da lógica do aplicativo, como funções críticas, para entender melhor o desempenho e os pontos de falha.

---

### **Testar a Instrumentação**

Abra o navegador em **http://localhost:8501** e interaja com a aplicação Streamlit. Por exemplo:

1. Clique no botão "Rolar o Dado".
2. Acompanhe os resultados exibidos na interface.
3. No console, observe os rastreamentos, métricas e logs gerados automaticamente.

---

### **Saída Esperada no Console**

**Exemplo de rastreamento gerado**:
```json
{
    "name": "streamlit request",
    "context": {
        "trace_id": "0xdb1fc322141e64eb84f5bd8a8b1c6d1f",
        "span_id": "0x5c2b0f851030d17d"
    },
    "attributes": {
        "http.method": "GET",
        "http.route": "/",
        "service.name": "dice-app"
    }
}
```

**Exemplo de métrica gerada**:
```json
{
    "name": "http.server.active_requests",
    "value": 1,
    "attributes": {
        "http.method": "GET",
        "http.route": "/",
        "http.status_code": 200
    }
}
```

---

### **Adicionando Instrumentação Manual**

Embora a instrumentação automática seja útil, ela captura apenas o tráfego nas bordas da aplicação (como requisições HTTP). Para monitorar detalhes internos, como execuções de funções ou interações específicas, é necessário adicionar instrumentação manual. Isso será abordado em um próximo tópico.

Agora sua aplicação Streamlit está instrumentada e pronta para ser monitorada!

---

### **Logfire: Uma Solução para Observabilidade em Python**

O **Logfire** é uma plataforma de observabilidade baseada no **OpenTelemetry**, projetada para desenvolvedores Python que buscam simplificar a coleta e visualização de dados de telemetria. Para engenheiros de dados, o Logfire oferece uma experiência altamente otimizada para aplicações como pipelines de ETL, APIs e automações, com suporte direto para frameworks e bibliotecas comuns.

#### **Como o Logfire Facilita o Monitoramento?**

1. **Instrumentação Simples e Intuitiva**:
   - O Logfire reduz a complexidade da configuração do OpenTelemetry. Por exemplo, ao usar SQLAlchemy ou FastAPI, a instrumentação ocorre com poucas linhas de código, sem necessidade de modificações extensas.

2. **Logs Estruturados e Contextualizados**:
   - Ao contrário de logs desordenados, o Logfire fornece logs estruturados que podem ser analisados diretamente com ferramentas como Pandas ou SQL, facilitando o diagnóstico de problemas em pipelines.

3. **Dashboards e Alertas**:
   - Oferece visualizações prontas para rastreamentos, métricas e logs, sem a necessidade de configurar um backend manualmente.

4. **Integrações com Python**:
   - Suporte nativo a bibliotecas populares como **SQLAlchemy**, **FastAPI**, **Boto3** e **Requests**. Isso significa que engenheiros podem monitorar desde uma chamada a APIs externas até o desempenho de um script de ETL que faz upload para o S3.

---

### **Casos de Uso do Logfire em ETLs e Pipelines**

#### **Monitoramento de Consultas SQL com SQLAlchemy**
Logfire ajuda a rastrear tempos de execução de queries, detectando gargalos e otimizando consultas mal estruturadas. Ele também captura logs de transações e erros.

#### **Rastreamento de Requisições em APIs com FastAPI**
Com a instrumentação de FastAPI, o Logfire fornece detalhes completos de cada requisição, incluindo tempo de resposta, erros e latência por endpoint.

#### **Monitoramento de Chamada a Serviços AWS com Boto3**
Ao integrar o Logfire com o Boto3, você pode monitorar chamadas a serviços como S3 e DynamoDB, capturando informações sobre latência, falhas e comportamento de resposta.

#### **Medição de Desempenho de Requisições com Requests**
Logfire mede o tempo de resposta de chamadas HTTP externas e ajuda a identificar endpoints lentos ou APIs que frequentemente retornam erros.

---

### **Por Que Escolher o Logfire?**

1. **Foco em Python**: Ferramentas e integração nativas para engenheiros que utilizam Python em aplicações de dados.
2. **Baseado no OpenTelemetry**: Compatível com padrões abertos e fácil de estender para outras linguagens e sistemas.
3. **Fácil Configuração**: Em menos de 10 minutos, você pode configurar rastreamentos e logs em sua aplicação.
4. **Insights Aprofundados**: Desde logs básicos até rastreamentos detalhados, tudo unificado em uma interface amigável.

---

### **Exemplo Prático com Logfire**

**Instrumentação de um Pipeline ETL:**

```python
import logfire
from sqlalchemy import create_engine
import requests
import boto3

# Configurando o Logfire
logfire.configure(api_key="sua-chave-logfire")

# Monitorando SQLAlchemy
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
engine = create_engine("postgresql://user:password@localhost/dbname")
SQLAlchemyInstrumentor().instrument(engine=engine)

# Pipeline ETL
def etl_pipeline():
    logfire.info("Iniciando pipeline ETL")

    # Consultando dados
    with logfire.span("Executando consulta SQL"):
        connection = engine.connect()
        result = connection.execute("SELECT * FROM tabela")
        logfire.info("Consulta finalizada", rows=len(result.fetchall()))

    # Chamando API externa
    with logfire.span("Chamando API externa"):
        response = requests.get("https://api.example.com/data")
        logfire.info("Dados recebidos", status=response.status_code)

    # Upload para S3
    with logfire.span("Fazendo upload para S3"):
        s3 = boto3.client("s3")
        s3.put_object(Bucket="meu-bucket", Key="arquivo.csv", Body="conteúdo")

    logfire.info("Pipeline concluído com sucesso")

etl_pipeline()
```

Com esse exemplo, você rastreará cada etapa do pipeline ETL, desde consultas SQL até chamadas a APIs externas e interações com o S3, visualizando os dados diretamente no painel do Logfire.