import time
import logfire

# Configuração do logfire
logfire.configure()

def extract():
    """Simula a extração de dados."""
    logfire.info("Log 1: Iniciando a etapa de Extração.")
    time.sleep(1)  # Simulação do tempo de extração
    data = {"id": 1, "value": 100}  # Dados simulados
    logfire.info(f"Log 2: Dados extraídos: {data}")
    return data

def transform(data):
    """Simula a transformação de dados."""
    logfire.info("Log 1: Iniciando a etapa de Transformação.")
    time.sleep(2)  # Simulação do tempo de transformação
    transformed_data = {key: str(value) for key, value in data.items()}  # Exemplo de transformação
    logfire.info(f"Log 2: Dados transformados: {transformed_data}")
    return transformed_data

def load(data):
    """Simula o carregamento de dados."""
    logfire.info("Log 1: Iniciando a etapa de Carregamento.")
    time.sleep(20)  # Simulação do tempo de carregamento
    logfire.info(f"Log 2: Dados carregados com sucesso: {data}")

def etl_pipeline():
    """Pipeline completo de ETL."""
    logfire.info("Iniciando o pipeline ETL.")
    with logfire.span("ETL Pipeline Execution"):
        # Extração
        raw_data = extract()
        # Transformação
        transformed_data = transform(raw_data)
        # Carregamento
        load(transformed_data)
    logfire.info("Pipeline ETL concluído com sucesso.")

if __name__ == "__main__":
    etl_pipeline()
