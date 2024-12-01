from datetime import datetime
from pydantic import BaseModel
import requests
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from time import sleep
import logfire

# Configuração do Logfire
logfire.configure()

# URL da API para buscar o valor atual do Bitcoin
URL = 'https://api.coinbase.com/v2/prices/spot?currency=USD'

# Configuração do banco de dados PostgreSQL remoto
POSTGRES_URI = "postgresql://dbname_mc8n_user:9Lhi7BqSDLhfUwRrJzJRZfUcKAs1qSYM@dpg-ct622rjv2p9s739531kg-a.ohio-postgres.render.com:5432/dbname_mc8n"

# Base declarativa do SQLAlchemy
Base = declarative_base()

# Configurar a engine globalmente
engine = create_engine(POSTGRES_URI, echo=False)  # echo=False para desativar logs detalhados de SQL
Base.metadata.create_all(engine)  # Cria as tabelas no banco de dados
logfire.info("Tabelas criadas no banco de dados (se não existiam).")

# Configurar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)

# Modelo da tabela usando SQLAlchemy
class BitcoinDataModel(Base):
    __tablename__ = "bitcoin_data"
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID incremental
    amount = Column(String, nullable=False)
    base = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)  # Timestamp com valor padrão

# Modelo Pydantic para validação de dados
class BitcoinData(BaseModel):
    amount: str
    base: str
    currency: str

class ApiResponse(BaseModel):
    data: BitcoinData

def test_connection():
    """Testa a conexão com o banco PostgreSQL."""
    try:
        with engine.connect() as conn:
            logfire.info("Conexão bem-sucedida com o banco PostgreSQL.")
    except Exception as e:
        logfire.error(f"Erro ao conectar ao banco de dados: {e}")

def extract():
    """Faz uma requisição à API para obter o valor do Bitcoin."""
    with logfire.span("Fazendo a requisição para obter o valor do Bitcoin"):
        response = requests.get(url=URL)
        return response.json()

def transform(data):
    """Valida os dados recebidos da API usando os modelos Pydantic."""
    with logfire.span("Validando os dados com Pydantic"):
        validated_data = ApiResponse(**data)
        return validated_data.model_dump()

def load(data):
    """Carrega os dados validados para um banco de dados PostgreSQL remoto usando SQLAlchemy."""
    with logfire.span("Carregando os dados no banco de dados PostgreSQL"):
        session = Session()
        bitcoin_entry = BitcoinDataModel(
            amount=data['data']['amount'],
            base=data['data']['base'],
            currency=data['data']['currency'],
            timestamp=datetime.utcnow()  # Adiciona o timestamp da inserção
        )
        session.add(bitcoin_entry)
        session.commit()
        logfire.info(
            "Dado inserido no banco: {amount} {base}/{currency} em {timestamp}",
            amount=bitcoin_entry.amount,
            base=bitcoin_entry.base,
            currency=bitcoin_entry.currency,
            timestamp=bitcoin_entry.timestamp,
        )
        session.close()

# Loop contínuo do pipeline ETL
logfire.info("Iniciando o loop do pipeline ETL. Pressione Ctrl+C para interromper.")
try:
    while True:
        with logfire.span("Execução completa do pipeline ETL"):
            raw_data = extract()
            transformed_data = transform(raw_data)
            load(transformed_data)
            logfire.info("Pipeline concluído. Aguardando 10 segundos antes de repetir.")
        sleep(10)  # Aguarda 10 segundos antes de repetir
except KeyboardInterrupt:
    logfire.info("Execução do pipeline interrompida pelo usuário.")
