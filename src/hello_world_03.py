from pydantic import BaseModel, ValidationError
import logfire
import requests

# Configuração do Logfire
logfire.configure()
logfire.instrument_requests()

# URL da API
URL = 'https://api.coinbase.com/v2/prices/spot?currency=USD'

# Modelo de validação com Pydantic
class BitcoinData(BaseModel):
    amount: str
    base: str
    currency: str

class ApiResponse(BaseModel):
    data: BitcoinData

def check_data(data):
    """
    Valida os dados usando Pydantic.
    Retorna os dados validados ou levanta uma exceção.
    """
    try:
        validated_data = ApiResponse(**data)
        logfire.info("Data validated successfully.")
        return validated_data
    except ValidationError as e:
        logfire.error(f"Validation error: {e}")
        return None

def extract():
    response = requests.get(url=URL)
    data_dict = response.json()

    # Validar os dados
    validated_data = check_data(data_dict)
    if validated_data:
        logfire.info(f"Bitcoin value: {validated_data.dict()}!")
        return validated_data.model_dump()
    else:
        logfire.warning("Invalid data received. Check the API or validation logic.")
        return None

# Chamada do pipeline
if __name__ == "__main__":
    print(extract())
