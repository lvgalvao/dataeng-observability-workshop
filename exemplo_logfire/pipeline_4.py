import logfire

from pipeline_2 import etl_pipeline


# Configuração do logfire
logfire.configure()
logfire.install_auto_tracing(modules=['app'], min_duration=0.01)

# Importa a função principal do módulo app

if __name__ == "__main__":
    etl_pipeline()
