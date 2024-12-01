from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)

# Configuração do tracer provider
tracer_provider = TracerProvider()
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
tracer_provider.add_span_processor(span_processor)
trace.set_tracer_provider(tracer_provider)

# Criação do tracer
tracer = trace.get_tracer("my.tracer.name")

# Configuração do meter provider para métricas
metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Criação do meter
meter = metrics.get_meter("my.meter.name")

# Definição do contador de métricas
work_counter = meter.create_counter(
    "work.counter", unit="1", description="Counts the amount of work done"
)

# Classe para simular um item de trabalho
class WorkItem:
    def __init__(self, work_type):
        self.work_type = work_type

# Função para executar trabalho com spans e métricas
def do_work(work_item):
    with tracer.start_as_current_span("parent") as parent:
        # Atributos e eventos no span 'parent'
        parent.set_attribute("operation.value", 1)
        parent.set_attribute("operation.name", "Saying hello!")
        parent.set_attribute("operation.other-stuff", [1, 2, 3])
        work_counter.add(1, {"work.type": work_item.work_type})
        parent.add_event("Gonna try it!")
        print("doing some work...")

        # Criar um span filho para trabalho aninhado
        with tracer.start_as_current_span("child") as child:
            # Atributos e eventos no span 'child'
            child.set_attribute("child.attribute", "child-value")
            child.add_event("Child span event")
            print("doing some nested work...")

# Executar o trabalho com um exemplo de WorkItem
work_item = WorkItem(work_type="example")
do_work(work_item)
