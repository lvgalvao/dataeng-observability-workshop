from opentelemetry.metrics import get_meter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# Configuração única do recurso e do provedor
resource = Resource(
    attributes={
        SERVICE_NAME: "pipeline-etl",
        "pipeline_id": "etl_sales_2025",
        "environment": "production",
        "team": "data_engineering",
    }
)

# Configuração do leitor de métricas e do provedor
reader_console = PeriodicExportingMetricReader(ConsoleMetricExporter())
reader_otlp = PeriodicExportingMetricReader(OTLPMetricExporter())
provider = MeterProvider(resource=resource, metric_readers=[reader_console, reader_otlp])

# Criar o 'meter' fora do ciclo do pipeline
meter = get_meter("etl_pipeline_meter", meter_provider=provider)

# Criar contador global para rastrear registros processados
counter = meter.create_counter(
    name="records_processed",
    description="Número de registros processados pelo pipeline ETL.",
    unit="1",  # Unidade em contagem
)

# Função para extração de dados
def extract():
    print("Extraindo dados...")
    extracted_data = ["record1", "record2", "record3", "record4"]
    # Atualizar contadores
    counter.add(amount=6, attributes={"status": "success", "stage": "extraction"})
    counter.add(amount=1, attributes={"status": "failure", "stage": "extraction"})
    return extracted_data

# Função para transformação de dados
def transform(data):
    print("Transformando dados...")
    transformed_data = [record.upper() for record in data if "record" in record]
    # Atualizar contadores
    counter.add(amount=2, attributes={"status": "success", "stage": "transformation"})
    counter.add(amount=1, attributes={"status": "failure", "stage": "transformation"})
    return transformed_data

# Função para carregamento de dados
def load(data):
    print("Carregando dados...")
    successful_loads = len(data) - 1  # Simular 1 falha
    failed_loads = 1
    # Atualizar contadores
    counter.add(amount=successful_loads, attributes={"status": "success", "stage": "loading"})
    counter.add(amount=failed_loads, attributes={"status": "failure", "stage": "loading"})

# Função para executar o pipeline
def run_pipeline():
    print("Iniciando pipeline ETL...")
    data = extract()  # Extração
    transformed_data = transform(data)  # Transformação
    load(transformed_data)  # Carregamento
    print("Pipeline concluída.")

run_pipeline()