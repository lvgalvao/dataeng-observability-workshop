from pydantic import BaseModel
import requests
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker

# URL da API para buscar o valor atual do Bitcoin
URL = 'https://api.coinbase.com/v2/prices/spot?currency=USD'

# Base declarativa do SQLAlchemy
Base = declarative_base()

# Modelo da tabela usando SQLAlchemy
class BitcoinDataModel(Base):
    __tablename__ = "bitcoin_data"
    amount = Column(String, primary_key=True)
    base = Column(String)
    currency = Column(String)

# Modelo Pydantic para validação de dados
class BitcoinData(BaseModel):
    amount: str
    base: str
    currency: str

class ApiResponse(BaseModel):
    data: BitcoinData

def extract():
    """Faz uma requisição à API para obter o valor do Bitcoin."""
    response = requests.get(url=URL)
    return response.json()

def transform(data):
    """Valida os dados recebidos da API usando os modelos Pydantic."""
    validated_data = ApiResponse(**data)
    return validated_data.model_dump()

def load(data):
    """Carrega os dados validados para um banco de dados SQLite em memória usando SQLAlchemy."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    bitcoin_entry = BitcoinDataModel(
        amount=data['data']['amount'],
        base=data['data']['base'],
        currency=data['data']['currency']
    )

    session.add(bitcoin_entry)
    session.commit()

    results = session.query(BitcoinDataModel).all()
    print("Dados armazenados no SQLite (via SQLAlchemy):")
    for result in results:
        print(f"Amount: {result.amount}, Base: {result.base}, Currency: {result.currency}")

    session.close()

# Executar o pipeline ETL
raw_data = extract()
transformed_data = transform(raw_data)
load(transformed_data)
