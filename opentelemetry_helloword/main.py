from opentelemetry.metrics import get_meter

from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
dotenv_path = '.env'  # Substitua pelo caminho do seu arquivo .env, se necessário
load_dotenv(dotenv_path=dotenv_path)

resource = Resource(attributes={SERVICE_NAME: "opentelemetry-helloword",
                                SERVICE_VERSION: "0.1.0"})

reader_console = PeriodicExportingMetricReader(
    exporter=ConsoleMetricExporter(),
    export_interval_millis=1000
)

reader_otlp = PeriodicExportingMetricReader(
    exporter=OTLPMetricExporter(),
    export_interval_millis=1000
)

provider = MeterProvider(resource=resource, metric_readers=[reader_console, reader_otlp])

meter = get_meter("meter", meter_provider=provider)

counter = meter.create_counter(
    name="carros.passando",
    unit="1",
    description="Carros passando na minha rua"
)
counter.add(
    amount=1, attributes={"modelo": "gol"}
)

counter.add(
    amount=1, attributes={"modelo": "monza"}
)


