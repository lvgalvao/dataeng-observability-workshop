from pydantic import BaseModel
import requests
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker

# URL da API para buscar o valor atual do Bitcoin
URL = 'https://api.coinbase.com/v2/prices/spot?currency=USD'

# Configuração do banco de dados PostgreSQL remoto
POSTGRES_URI = "postgresql://dbname_mc8n_user:9Lhi7BqSDLhfUwRrJzJRZfUcKAs1qSYM@dpg-ct622rjv2p9s739531kg-a.ohio-postgres.render.com:5432/dbname_mc8"

# Base declarativa do SQLAlchemy
Base = declarative_base()

# Configurar a engine globalmente
engine = create_engine(POSTGRES_URI, echo=True)  # echo=True para mostrar logs de SQL
Base.metadata.create_all(engine)  # Cria as tabelas no banco de dados

# Configurar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)

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
    """Carrega os dados validados para um banco de dados PostgreSQL remoto usando SQLAlchemy."""
    session = Session()

    bitcoin_entry = BitcoinDataModel(
        amount=data['data']['amount'],
        base=data['data']['base'],
        currency=data['data']['currency']
    )

    session.add(bitcoin_entry)
    session.commit()

    results = session.query(BitcoinDataModel).all()
    print("Dados armazenados no PostgreSQL:")
    for result in results:
        print(f"Amount: {result.amount}, Base: {result.base}, Currency: {result.currency}")

    session.close()

# Executar o pipeline ETL
raw_data = extract()
transformed_data = transform(raw_data)
load(transformed_data)
