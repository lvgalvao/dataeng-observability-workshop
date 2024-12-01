from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

# Configuração do tracer provider
provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Criação do tracer
tracer = trace.get_tracer("my.tracer.name")

def do_work():
    with tracer.start_as_current_span("parent") as parent:
        # Atributos e eventos no span 'parent'
        parent.set_attribute("operation.value", 1)
        parent.set_attribute("operation.name", "Saying hello!")
        parent.set_attribute("operation.other-stuff", [1, 2, 3])
        parent.add_event("Gonna try it!")
        print("doing some work...")

        # Criar um span filho para trabalho aninhado
        with tracer.start_as_current_span("child") as child:
            # Atributos e eventos no span 'child'
            child.set_attribute("child.attribute", "child-value")
            child.add_event("Child span event")
            print("doing some nested work...")

do_work()
