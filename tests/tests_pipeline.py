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
