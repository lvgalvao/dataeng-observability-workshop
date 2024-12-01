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
