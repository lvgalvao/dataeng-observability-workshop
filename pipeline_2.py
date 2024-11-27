import time
import logfire


def extract():
    """Simula a extração de dados."""
    time.sleep(1)  # Simulação do tempo de extração
    data = {"id": 1, "value": 100}  # Dados simulados
    return data

def transform(data):
    """Simula a transformação de dados."""
    time.sleep(2)  # Simulação do tempo de transformação
    transformed_data = {key: str(value) for key, value in data.items()}  # Exemplo de transformação
    return transformed_data

def load(data):
    """Simula o carregamento de dados."""
    logfire.info("Log 1: Iniciando a etapa de Carregamento.")
    time.sleep(1)  # Simulação do tempo de carregamento

def etl_pipeline():
    """Pipeline completo de ETL."""
        # Extração
    raw_data = extract()
        # Transformação
    transformed_data = transform(raw_data)
        # Carregamento
    load(transformed_data)

if __name__ == "__main__":
    etl_pipeline()
