# Instrumentação manual

As diferenças entre `opentelemetry-distro` e `opentelemetry-exporter-otlp` estão relacionadas à função de cada pacote no ecossistema do OpenTelemetry. Vamos detalhar:

---

### **1. opentelemetry-distro**
- **Função**: 
  - É um pacote de "distribuição" que facilita a configuração e inicialização do OpenTelemetry.
  - Ele reúne um conjunto de dependências e implementa boas práticas para configurar o SDK do OpenTelemetry.
- **Características**:
  - Configura automaticamente **tracing** e **metrics**.
  - Simplifica a integração com outros componentes do OpenTelemetry, como **instrumentação automática** (autoinstrumentation).
  - Oferece uma maneira padrão de iniciar sua aplicação com OpenTelemetry já preparado para enviar dados para exportadores.
- **Uso**:
  - Usado por quem quer evitar configurações complexas e começar rapidamente com uma implementação padrão.
  - Exemplo: Configurar rastreamento automático de uma aplicação web.

---

### **2. opentelemetry-exporter-otlp**
- **Função**:
  - É um **exportador**, responsável por enviar os dados coletados pelo SDK do OpenTelemetry (traces e métricas) para um backend específico, utilizando o protocolo OTLP (**OpenTelemetry Protocol**).
- **Características**:
  - Focado exclusivamente no envio de dados para o backend.
  - Funciona como um "conector" entre sua aplicação instrumentada e serviços como Logfire, New Relic, Jaeger, Grafana, ou outros que suportam OTLP.
- **Uso**:
  - Deve ser configurado junto com o SDK ou com `opentelemetry-distro` para exportar os dados para o serviço de observabilidade escolhido.
  - Exemplo: Exportar traces e métricas para um backend de observabilidade usando o protocolo OTLP.

---

### **Comparação em um projeto**
- **`opentelemetry-distro`**:
  - É a configuração "base", onde você prepara o OpenTelemetry para começar a coletar dados.
  - Inclui configuração do SDK e inicialização dos componentes.

- **`opentelemetry-exporter-otlp`**:
  - É um componente adicional que conecta os dados coletados a um backend específico.

---

### **Exemplo Prático**
1. **Instalar os pacotes necessários**:
   ```bash
   pip install opentelemetry-distro
   ```

Aqui está um exemplo mais detalhado, focado em um contexto de **engenharia de dados**, com atributos adicionais para enriquecer a explicação e ilustrar como o OpenTelemetry pode ser usado para monitorar métricas em pipelines de dados:

---

### **Exemplo: Monitorando um Pipeline de ETL com OpenTelemetry Metrics**

Imagine que você está construindo um pipeline de ETL para processar dados de vendas em lote. Deseja monitorar quantos registros foram processados e acompanhar métricas específicas.

#### **Código**

```python
from opentelemetry.metrics import get_meter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Configurar recurso do OpenTelemetry
resource = Resource(
    attributes={
        SERVICE_NAME: "pipeline-etl",
        "pipeline_id": "etl_sales_2025",
        "environment": "production",
        "team": "data_engineering",
    }
)

# Configurar leitor de métricas e provedor
reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
provider = MeterProvider(resource=resource, metric_readers=[reader])

# Criar o 'meter'
meter = get_meter("etl_pipeline_meter", meter_provider=provider)

# Criar contador para rastrear o número de registros processados
counter = meter.create_counter(
    name="records_processed",
    description="Número de registros processados pelo pipeline ETL.",
    unit="1",  # Contagem
)

# Função: Extração de dados
def extract():
    print("Extraindo dados...")
    extracted_data = ["record1", "record2", "record3", "record4"]
    # Simular sucesso e falha na extração
    counter.add(amount=3, attributes={"status": "success", "stage": "extraction"})
    counter.add(amount=1, attributes={"status": "failure", "stage": "extraction"})
    return extracted_data

# Função: Transformação de dados
def transform(data):
    print("Transformando dados...")
    transformed_data = [record.upper() for record in data if "record" in record]
    # Simular sucesso e falha na transformação
    counter.add(amount=2, attributes={"status": "success", "stage": "transformation"})
    counter.add(amount=1, attributes={"status": "failure", "stage": "transformation"})
    return transformed_data

# Função: Carregamento de dados
def load(data):
    print("Carregando dados...")
    # Simular carregamento de dados
    successful_loads = len(data) - 1  # Simular 1 falha
    failed_loads = 1
    counter.add(amount=successful_loads, attributes={"status": "success", "stage": "loading"})
    counter.add(amount=failed_loads, attributes={"status": "failure", "stage": "loading"})

# Função: Pipeline completa
def run_pipeline():
    print("Iniciando pipeline ETL...")
    data = extract()  # Extração
    transformed_data = transform(data)  # Transformação
    load(transformed_data)  # Carregamento
    print("Pipeline concluída.")

# Executar pipeline
run_pipeline()
```

---

### **Explicação Detalhada**

#### **1. `Resource`**
- Representa metadados sobre o serviço monitorado.
- **Atributos incluídos**:
  - `SERVICE_NAME`: Nome do serviço, neste caso, o pipeline ETL.
  - `pipeline_id`: Identificador único do pipeline.
  - `environment`: Ambiente em que o pipeline está rodando (produção, desenvolvimento etc.).
  - `team`: Equipe responsável pelo pipeline.

---

#### **2. `MeterProvider`**
- Configura o provedor de métricas, incluindo:
  - **Leitores de métricas (`metric_readers`)**: Responsáveis por exportar as métricas.
  - **Exportadores**:
    - No exemplo, o `ConsoleMetricExporter` exporta métricas para o console (simples para debugging).

---

#### **3. `Counter`**
- Um contador é usado para medir eventos acumulativos, como o número de registros processados.
- **Parâmetros importantes**:
  - `name`: Nome da métrica (ex.: `records_processed`).
  - `description`: Descrição para entendimento do propósito (ex.: "Número de registros processados pelo pipeline ETL").
  - `unit`: Unidade de medida, aqui `1` indica contagem. Pode ser "bytes", "ms" etc., dependendo da métrica.

---

#### **4. Atributos nos `add`**
- Atributos contextualizam as métricas.
- **No exemplo**:
  - `status`: Indica se a execução foi um sucesso ou falhou.
  - `stage`: Mostra em qual estágio do pipeline a métrica foi registrada (extração, transformação, carregamento).

---

### **Saída esperada (Console)**

O exportador de console exibirá as métricas como:

```
Resource Attributes: {'service.name': 'pipeline-etl', 'pipeline_id': 'etl_sales_2025', 'environment': 'production', 'team': 'data_engineering'}
Metric Export: {'name': 'records_processed', 'value': 100, 'attributes': {'status': 'success', 'stage': 'extraction'}}
Metric Export: {'name': 'records_processed', 'value': 20, 'attributes': {'status': 'failure', 'stage': 'extraction'}}
Metric Export: {'name': 'records_processed', 'value': 80, 'attributes': {'status': 'success', 'stage': 'transformation'}}
Metric Export: {'name': 'records_processed', 'value': 10, 'attributes': {'status': 'failure', 'stage': 'transformation'}}
Metric Export: {'name': 'records_processed', 'value': 70, 'attributes': {'status': 'success', 'stage': 'loading'}}
Metric Export: {'name': 'records_processed', 'value': 5, 'attributes': {'status': 'failure', 'stage': 'loading'}}
```

---

### **Como isso ajuda em Engenharia de Dados**
1. **Monitoramento detalhado**: Permite identificar gargalos (ex.: falhas na transformação).
2. **Atributos ricos**: Contextualizam o comportamento do pipeline com dimensões importantes (ex.: status, estágio).
3. **Integração fácil**: Pode ser configurado para enviar dados para ferramentas de observabilidade (Grafana, Prometheus, etc.).

Este exemplo mostra como o OpenTelemetry pode ser usado para capturar métricas úteis em pipelines ETL e fornecer visibilidade detalhada para engenheiros de dados.

## Jogando para o backend local

```bash
pip install opentelemetry-exporter-otlp
```

```python
from opentelemetry.metrics import get_meter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# Configurar recurso do OpenTelemetry
resource = Resource(
    attributes={
        SERVICE_NAME: "pipeline-etl",
        "pipeline_id": "etl_sales_2025",
        "environment": "production",
        "team": "data_engineering",
    }
)

# Configurar leitor de métricas e provedor
reader_console = PeriodicExportingMetricReader(ConsoleMetricExporter())
reader_otlp = PeriodicExportingMetricReader(OTLPMetricExporter())
provider = MeterProvider(resource=resource, metric_readers=[reader_console, reader_otlp])

# Criar o 'meter'
meter = get_meter("etl_pipeline_meter", meter_provider=provider)

# Criar contador para rastrear o número de registros processados
counter = meter.create_counter(
    name="records_processed",
    description="Número de registros processados pelo pipeline ETL.",
    unit="1",  # Contagem
)

# Função: Extração de dados
def extract():
    print("Extraindo dados...")
    extracted_data = ["record1", "record2", "record3", "record4"]
    # Simular sucesso e falha na extração
    counter.add(amount=3, attributes={"status": "success", "stage": "extraction"})
    counter.add(amount=1, attributes={"status": "failure", "stage": "extraction"})
    return extracted_data

# Função: Transformação de dados
def transform(data):
    print("Transformando dados...")
    transformed_data = [record.upper() for record in data if "record" in record]
    # Simular sucesso e falha na transformação
    counter.add(amount=2, attributes={"status": "success", "stage": "transformation"})
    counter.add(amount=1, attributes={"status": "failure", "stage": "transformation"})
    return transformed_data

# Função: Carregamento de dados
def load(data):
    print("Carregando dados...")
    # Simular carregamento de dados
    successful_loads = len(data) - 1  # Simular 1 falha
    failed_loads = 1
    counter.add(amount=successful_loads, attributes={"status": "success", "stage": "loading"})
    counter.add(amount=failed_loads, attributes={"status": "failure", "stage": "loading"})

# Função: Pipeline completa
def run_pipeline():
    print("Iniciando pipeline ETL...")
    data = extract()  # Extração
    transformed_data = transform(data)  # Transformação
    load(transformed_data)  # Carregamento
    print("Pipeline concluída.")

# Executar pipeline
run_pipeline()
```

Ao rodar isso vamos ver erros uma vez que não temos o backend configurado.

Atualizando o exemplo para enviar para o backend local.

Precisamso rodar o compose para subir o backend local.

```bash
docker compose up
```

```yml
services:
  olgtm:
    image: grafana/otel-lgtm
    ports:
      - 3000:3000  # grafana (admin, admin)
      - 9090:9090  # prometheus
      - 4318:4318  # collector http
      - 4317:4317  # collector grpc
```

Agora vamos rodar o exemplo 01 novamente.

Abrir o prometheus no navegador `http://localhost:9090/` e ver as métricas sendo enviadas.

Ele vai ter criado um `records_processed_total` que é a soma de todos os registros processados. 
Queremos calcular a soma total de todos os registros processados em todos os estágios e independentemente do status. `sum(records_processed_total)`

Queremos calcular a soma de todos os registros processados para um estágio específico, como "extraction". `sum(records_processed_total{stage="extraction"})`

Queremos calcular a porcentagem de falha para um estágio específico, como "extraction". `100 * sum(records_processed_total{status="failure", stage="extraction"}) / sum(records_processed_total{stage="extraction"})`

Olhar também o gráfico.

### **Instrumentação Automática no OpenTelemetry**

A instrumentação automática é uma das funcionalidades mais poderosas do OpenTelemetry. Ela permite monitorar e coletar métricas ou traces de aplicações sem modificar diretamente o código-fonte, bastando ativar plugins de instrumentação adequados. Isso é particularmente útil para frameworks ou bibliotecas comuns, como Flask, Django, SQLAlchemy, ou mesmo bibliotecas de HTTP.

---

### **1. O que é Instrumentação Automática?**

- **Como funciona?**
  - A instrumentação automática utiliza "wrappers" ou interceptadores (hooks) nas bibliotecas que você já está usando para capturar eventos e criar spans ou métricas automaticamente.

- **Vantagens**:
  - Menor esforço de implementação, pois não é necessário adicionar instrumentação manual no código.
  - Integração consistente e padrão para diferentes bibliotecas e frameworks.
  - Ideal para rastrear interações entre serviços ou bibliotecas.

- **Desvantagens**:
  - Menor flexibilidade em casos de instrumentação altamente personalizada.
  - Pode adicionar overhead dependendo da configuração.

---

### **2. O Repositório `opentelemetry-python-contrib`**

O repositório [opentelemetry-python-contrib](https://github.com/open-telemetry/opentelemetry-python-contrib) é um hub para plugins de instrumentação automática. Ele fornece suporte para várias bibliotecas e frameworks populares.

#### **Exemplos de instrumentação disponíveis**:
- **Frameworks Web**: Flask, Django, FastAPI.
- **Bibliotecas de Banco de Dados**: SQLAlchemy, psycopg2, mysql-connector.
- **HTTP**: Requests, urllib.
- **Mensageria**: Kafka, RabbitMQ.

#### **Como instalar um plugin?**
Você pode instalar plugins para instrumentação automática usando pip. Por exemplo:

```bash
pip install opentelemetry-instrumentation-flask
pip install opentelemetry-instrumentation-sqlalchemy
```

---

### **3. Configurando o Exemplo Anterior com Instrumentação Automática**

Vamos configurar o pipeline ETL para instrumentação automática usando o `opentelemetry-instrument` CLI.

#### **Passo 1: Instale os Pacotes Necessários**
```bash
pip install opentelemetry-distro
pip install opentelemetry-instrumentation
pip install opentelemetry-exporter-otlp
```

Opcionalmente, adicione instrumentação para bibliotecas específicas:
```bash
pip install opentelemetry-instrumentation-requests
pip install opentelemetry-instrumentation-urllib
```

---

#### **Passo 2: Configurar Instrumentação Automática**
1. **Adicione um exportador de OTLP para capturar as métricas e traces.**
2. **Inicie a aplicação usando `opentelemetry-instrument`.**

Atualize o script do exemplo anterior para suportar o exportador OTLP e não adicione manualmente spans no código.

#### **Script Atualizado**
```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configurar o exportador OTLP
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
trace.set_tracer_provider(TracerProvider())
tracer_provider = trace.get_tracer_provider()
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

# Exemplo de uma função no pipeline
def extract():
    print("Extraindo dados...")
    return ["record1", "record2", "record3", "record4"]

def transform(data):
    print("Transformando dados...")
    return [record.upper() for record in data]

def load(data):
    print("Carregando dados...")
    print(f"Dados carregados: {data}")

def run_pipeline():
    print("Iniciando pipeline ETL...")
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)
    print("Pipeline concluída.")

if __name__ == "__main__":
    run_pipeline()
```

---

#### **Passo 3: Executar com Instrumentação Automática**
Execute o script usando o comando `opentelemetry-instrument`:

```bash
opentelemetry-instrument python pipeline.py
```

#### **O que acontece?**
1. **Instrumentação Automática**:
   - Se o pipeline faz chamadas HTTP, usa banco de dados, ou qualquer biblioteca suportada, os spans e métricas serão coletados automaticamente.
2. **Traces e Métricas**:
   - As informações coletadas serão enviadas para o endpoint configurado (ex.: OTLP no `localhost:4317`).
3. **Métricas e logs no console**:
   - Métricas e spans podem ser visualizados em ferramentas como Jaeger, Prometheus, ou Grafana.

---

### **4. Benefícios para o Exemplo de ETL**
Com instrumentação automática:
- Você pode rastrear as interações entre os estágios do pipeline (`extract`, `transform`, `load`) sem modificar diretamente o código.
- Detalhes de dependências, como chamadas HTTP ou operações de banco de dados, são automaticamente capturados.
- É ideal para sistemas de ETL que usam várias bibliotecas de terceiros.

---

### **Resumo**
- **Automático**: A instrumentação automática é rápida de configurar e ideal para rastrear frameworks e bibliotecas comuns.
- **Personalização Manual**: É mais flexível, mas exige alterações no código.

Usar a instrumentação automática reduz significativamente o trabalho inicial e permite uma visão geral consistente de todo o sistema. Em casos avançados, você pode combinar as duas abordagens para obter o melhor de ambos os mundos.

