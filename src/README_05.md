# **README: Pipeline ETL com Logfire e PostgreSQL**

## **Descrição**
Este projeto implementa um pipeline ETL simples que realiza as seguintes operações:
1. **Extract (Extração)**: Obtém o preço atual do Bitcoin usando a API da Coinbase.
2. **Transform (Transformação)**: Valida os dados da API usando Pydantic para garantir a integridade.
3. **Load (Carga)**: Armazena os dados validados em um banco de dados PostgreSQL remoto.

Além disso, a aplicação está integrada ao **Logfire** para monitoramento, rastreamento (tracing) e métricas, permitindo uma análise detalhada do desempenho e status do pipeline.

---

## **Instalação**

1. **Clone o Repositório**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Instale as Dependências**
   Certifique-se de que o Python 3.9 ou superior está instalado.
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o Banco de Dados PostgreSQL**
   Atualize a variável `POSTGRES_URI` no código com as credenciais do seu banco de dados PostgreSQL.

---

## **Execução**

### **Rodar o Pipeline**
Basta executar o script principal para iniciar o pipeline ETL em loop contínuo:
```bash
python main.py
```
- O pipeline executará automaticamente a cada 10 segundos.
- Pressione `Ctrl+C` para interromper.

---

## **Estrutura do Código**

### **1. Configuração de Logfire**
- **Instrumentação Automática**: `logfire.instrument_requests()` e `logfire.instrument_sqlalchemy()` são usados para rastrear automaticamente requisições HTTP e transações SQL.
- **Atributos Customizados**: Cada operação do pipeline insere atributos estruturados para facilitar consultas no Logfire Explore.

### **2. Pipeline ETL**
O pipeline é dividido em três etapas principais:

#### **Extract**
Faz uma requisição à API da Coinbase e registra informações como:
- Código de status HTTP (`http_response_status_code`).
- Endpoint consultado.

#### **Transform**
Valida os dados recebidos da API com Pydantic, garantindo que estejam no formato correto. Registra atributos como:
- Valor do Bitcoin (`amount`).
- Moeda base e de destino (`base` e `currency`).

#### **Load**
Insere os dados validados no banco de dados PostgreSQL e registra:
- Detalhes do banco (`database`).
- Timestamp de inserção.

### **3. Monitoramento com Logfire**
O uso de spans e métricas no Logfire permite:
- Monitorar o desempenho de cada etapa do pipeline.
- Rastrear erros ou exceções com atributos detalhados.

---

## **Métricas Implementadas**

### **1. Atributos no Logfire**
Os atributos registrados em cada operação permitem consultas detalhadas:
- **`span_name`**: Identifica a etapa do pipeline (`extract`, `transform`, `load`).
- **`otel_status_code`**: Indica o status de sucesso ou erro (`OK`, `ERROR`).
- **`http_response_status_code`**: Código de resposta da API na etapa `extract`.
- **`database`**: Nome do banco usado na etapa `load`.

### **2. Métricas Customizadas**
- **Contador de Execuções**: Número de execuções bem-sucedidas do pipeline.
- **Duração de Cada Etapa**: Métrica de tempo para as operações `extract`, `transform`, e `load`.
- **Erros HTTP**: Número de respostas com erro na API (`http_response_status_code != 200`).
- **Registros Inseridos no Banco**: Número de inserções bem-sucedidas.
- **Timestamps**: Controle do tempo exato de cada operação.

---

## **Consultas no Logfire Explore**

### **1. Filtrar Etapa Específica**
Para consultar logs da etapa `extract`:
```sql
SELECT *
FROM records
WHERE attributes->>'span_name' = 'extract';
```

### **2. Consultar Erros**
Logs de operações com erros:
```sql
SELECT *
FROM records
WHERE attributes->>'otel_status_code' = 'ERROR';
```

### **3. Consultar Respostas HTTP 200**
Filtrar logs com respostas bem-sucedidas da API:
```sql
SELECT *
FROM records
WHERE attributes->>'http_response_status_code' = '200';
```

### **4. Consultar Dados Inseridos**
Ver registros com detalhes dos dados inseridos no banco:
```sql
SELECT attributes->>'amount', attributes->>'base', attributes->>'currency', attributes->>'timestamp'
FROM records
WHERE attributes->>'span_name' = 'load';
```

---

## **Benefícios do Logfire**
1. **Monitoramento em Tempo Real**: Todos os logs, spans e métricas podem ser visualizados em tempo real no Logfire Explore.
2. **Estruturação de Dados**: Os atributos estruturados permitem consultas flexíveis com SQL.
3. **Integração Simples**: Com poucas linhas de código, o Logfire rastreia e monitora automaticamente requisições e transações.

---

### **Exemplo de Saída de Logs no Console**
```plaintext
2024-12-01T10:00:00   Conexão bem-sucedida com o banco PostgreSQL.
2024-12-01T10:00:10   Requisição concluída. HTTP 200.
2024-12-01T10:00:11   Transformação concluída. Valor: 42000 USD.
2024-12-01T10:00:12   Dados inseridos no banco. ID: 1, Amount: 42000, Timestamp: 2024-12-01T10:00:12Z.
2024-12-01T10:00:13   Pipeline concluído. Aguardando 10 segundos antes de repetir.
```

---

## **Contribuindo**
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

### **Contato**
Em caso de dúvidas ou sugestões, entre em contato via e-mail: `email@exemplo.com`.