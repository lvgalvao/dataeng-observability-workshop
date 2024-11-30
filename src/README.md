### Arquivo: `pipeline.py`

```python
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
```

---

### Arquivo: `tests_pipeline.py`

```python
import pytest
from unittest.mock import patch
from pipeline import extract, check_data, ApiResponse

# Teste 1: Validação de dados corretos
def test_check_data_valid():
    valid_data = {
        "data": {
            "amount": "97054.355",
            "base": "BTC",
            "currency": "USD"
        }
    }
    validated = check_data(valid_data)
    assert validated is not None
    assert validated.data.amount == "97054.355"
    assert validated.data.base == "BTC"
    assert validated.data.currency == "USD"

# Teste 2: Validação de dados incorretos
def test_check_data_invalid():
    invalid_data = {
        "data": {
            "base": "BTC",
            "currency": "USD"
            # "amount" está ausente
        }
    }
    validated = check_data(invalid_data)
    assert validated is None

# Teste 3: Extração de dados válidos da API
@patch("pipeline.requests.get")
def test_extract_valid(mock_get):
    mock_get.return_value.json.return_value = {
        "data": {
            "amount": "97054.355",
            "base": "BTC",
            "currency": "USD"
        }
    }
    result = extract()
    assert result is not None
    assert result["data"]["amount"] == "97054.355"
    assert result["data"]["base"] == "BTC"
    assert result["data"]["currency"] == "USD"

# Teste 4: Extração de dados inválidos da API
@patch("pipeline.requests.get")
def test_extract_invalid(mock_get):
    mock_get.return_value.json.return_value = {
        "data": {
            "base": "BTC",
            "currency": "USD"
            # "amount" está ausente
        }
    }
    result = extract()
    assert result is None

# Teste 5: Erro de conexão na API
@patch("pipeline.requests.get")
def test_extract_api_error(mock_get):
    mock_get.side_effect = Exception("API error")
    result = extract()
    assert result is None
```

---

### Explicação do Código

#### `pipeline.py`

1. **Configuração do Logfire**:
   - `logfire.configure()` e `logfire.instrument_requests()` inicializam o monitoramento e o logging de requisições.

2. **Validação de Dados com Pydantic**:
   - `BitcoinData` e `ApiResponse` definem a estrutura esperada dos dados da API.
   - A função `check_data` valida os dados recebidos contra esses modelos, garantindo consistência e integridade.

3. **Extração de Dados**:
   - `extract` faz a requisição à API e valida os dados.
   - Em caso de erro na API ou dados inválidos, mensagens apropriadas são registradas nos logs.

#### `tests_pipeline.py`

1. **Testes para `check_data`**:
   - `test_check_data_valid`: Confirma que dados válidos passam pela validação.
   - `test_check_data_invalid`: Garante que dados ausentes ou malformados falhem na validação.

2. **Testes para `extract`**:
   - `test_extract_valid`: Simula uma resposta válida da API e verifica que a função retorna os dados corretamente.
   - `test_extract_invalid`: Testa se a função lida adequadamente com dados inválidos da API.
   - `test_extract_api_error`: Simula uma exceção no `requests.get` e garante que a função trate o erro.

---

### Estrutura do Projeto

```plaintext
project/
├── pipeline.py          # Código principal
├── tests_pipeline.py    # Testes unitários
└── requirements.txt     # Dependências
```

---

### Dependências

Crie um arquivo `requirements.txt` com as seguintes linhas:

```plaintext
pytest
pytest-mock
pydantic
logfire
requests
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

### Instruções para Rodar o Projeto

1. **Configurar o Ambiente**:
   - Certifique-se de estar na raiz do projeto.
   - Exporte o `PYTHONPATH` (se necessário):
     ```bash
     export PYTHONPATH=.
     ```

2. **Executar o Script**:
   - Para executar o script principal:
     ```bash
     python pipeline.py
     ```

3. **Executar os Testes**:
   - Use o comando abaixo para rodar todos os testes:
     ```bash
     pytest -v tests_pipeline.py
     ```

4. **Resultados Esperados**:
   - Os testes devem passar, validando que o código lida corretamente com cenários de sucesso, falha e exceções.

---

### Como um Engenheiro de Software Senior Validaria
- **Modularidade**: Cada função tem uma responsabilidade bem definida, seguindo o princípio SRP (Single Responsibility Principle).
- **Robustez**: Uso de Pydantic para validação garante que erros nos dados sejam capturados rapidamente.
- **Testabilidade**: O código é testável devido ao uso de mocks para simular respostas da API.
- **Logging**: Logs detalhados tornam o monitoramento e a depuração mais eficientes.