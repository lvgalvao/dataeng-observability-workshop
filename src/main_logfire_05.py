from datetime import datetime, timezone
from pydantic import BaseModel
import requests
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from time import sleep
import logfire

# Configuração do Logfire
logfire.configure()

# Instrumentação automática
logfire.instrument_requests()
logfire.instrument_sqlalchemy()

# URL da API para buscar o valor atual do Bitcoin
URL = 'https://api.coinbase.com/v2/prices/spot?currency=USD'

# Configuração do banco de dados PostgreSQL remoto
POSTGRES_URI = "postgresql://dbname_mc8n_user:9Lhi7BqSDLhfUwRrJzJRZfUcKAs1qSYM@dpg-ct622rjv2p9s739531kg-a.ohio-postgres.render.com:5432/dbname_mc8n"

# Base declarativa do SQLAlchemy
Base = declarative_base()

# Configurar a engine globalmente
engine = create_engine(POSTGRES_URI, echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# Modelo da tabela usando SQLAlchemy
class BitcoinDataModel(Base):
    __tablename__ = "bitcoin_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(String, nullable=False)
    base = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

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
            logfire.info("Conexão bem-sucedida com o banco PostgreSQL.", attributes={
                "otel_status_code": "OK",
                "database": "PostgreSQL"
            })
    except Exception as e:
        logfire.error("Erro ao conectar ao banco de dados.", attributes={
            "otel_status_code": "ERROR",
            "otel_status_message": str(e),
            "database": "PostgreSQL"
        })

def extract():
    """Faz uma requisição à API para obter o valor do Bitcoin."""
    with logfire.span("Fazendo a requisição para obter o valor do Bitcoin") as span:
        response = requests.get(url=URL)
        span.set_attribute("http_response_status_code", response.status_code)
        logfire.info("Requisição concluída.", attributes={
            "span_name": "extract",
            "http_response_status_code": response.status_code,
            "otel_status_code": "OK" if response.status_code == 200 else "ERROR",
            "endpoint": URL
        })
        return response.json()

def transform(data):
    """Valida os dados recebidos da API usando os modelos Pydantic."""
    with logfire.span("Validando os dados com Pydantic") as span:
        validated_data = ApiResponse(**data)
        span.set_attribute("amount", validated_data.data.amount)
        span.set_attribute("currency", validated_data.data.currency)
        logfire.info("Transformação concluída.", attributes={
            "span_name": "transform",
            "amount": validated_data.data.amount,
            "currency": validated_data.data.currency,
            "otel_status_code": "OK"
        })
        return validated_data.model_dump()

def load(data):
    """Carrega os dados validados para um banco de dados PostgreSQL remoto usando SQLAlchemy."""
    with logfire.span("Carregando os dados no banco de dados PostgreSQL") as span:
        session = Session()
        bitcoin_entry = BitcoinDataModel(
            amount=data['data']['amount'],
            base=data['data']['base'],
            currency=data['data']['currency'],
            timestamp=datetime.now(timezone.utc)
        )
        session.add(bitcoin_entry)
        session.commit()
        span.set_attribute("database", "PostgreSQL")
        span.set_attribute("amount", bitcoin_entry.amount)
        span.set_attribute("currency", bitcoin_entry.currency)
        logfire.info(
            "Dados inseridos no banco.",
            attributes={
                "span_name": "load",
                "amount": bitcoin_entry.amount,
                "base": bitcoin_entry.base,
                "currency": bitcoin_entry.currency,
                "timestamp": bitcoin_entry.timestamp.isoformat(),
                "otel_status_code": "OK",
                "database": "PostgreSQL"
            }
        )
        session.close()

# Loop contínuo do pipeline ETL
logfire.info("Iniciando o loop do pipeline ETL. Pressione Ctrl+C para interromper.", attributes={
    "otel_status_code": "START",
    "pipeline_name": "ETL_Bitcoin",
    "interval_seconds": 10
})
try:
    while True:
        with logfire.span("Execução completa do pipeline ETL") as span:
            raw_data = extract()
            transformed_data = transform(raw_data)
            load(transformed_data)
            logfire.info("Pipeline concluído. Aguardando 10 segundos antes de repetir.", attributes={
                "otel_status_code": "OK",
                "pipeline_name": "ETL_Bitcoin",
                "interval_seconds": 10
            })
        sleep(10)
except KeyboardInterrupt:
    logfire.info("Execução do pipeline interrompida pelo usuário.", attributes={
        "otel_status_code": "INTERRUPTED",
        "pipeline_name": "ETL_Bitcoin"
    })
