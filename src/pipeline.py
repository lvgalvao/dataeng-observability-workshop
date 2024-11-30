from pydantic import BaseModel, ValidationError
import logfire
import requests

# Configuração do Logfire para monitoramento e logging
logfire.configure()
logfire.instrument_requests()

# URL da API para buscar o valor atual do Bitcoin
URL = 'https://api.coinbase.com/v2/prices/spot?currency=USD'

# Modelos Pydantic para validação de dados
class BitcoinData(BaseModel):
    amount: str
    base: str
    currency: str

class ApiResponse(BaseModel):
    data: BitcoinData

def check_data(data):
    """
    Valida os dados recebidos da API usando os modelos Pydantic.
    
    :param data: Dicionário com os dados retornados da API.
    :return: Instância validada de ApiResponse ou None em caso de erro.
    """
    try:
        validated_data = ApiResponse(**data)
        logfire.info("Data validated successfully.")
        return validated_data
    except ValidationError as e:
        logfire.error(f"Validation error: {e}")
        return None

def extract():
    """
    Faz uma requisição à API para obter o valor do Bitcoin e valida os dados retornados.

    :return: Dicionário com os dados validados ou None se a validação falhar.
    """
    try:
        response = requests.get(url=URL)
        response.raise_for_status()  # Levanta exceções para erros HTTP
        data_dict = response.json()
        validated_data = check_data(data_dict)
        if validated_data:
            logfire.info(f"Bitcoin value: {validated_data.dict()}!")
            return validated_data.dict()
        else:
            logfire.warning("Invalid data received. Check the API or validation logic.")
            return None
    except Exception as e:
        logfire.error(f"Error during data extraction: {e}")
        return None

if __name__ == "__main__":
    print(extract())
