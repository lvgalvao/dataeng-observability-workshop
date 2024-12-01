### **README Atualizado com Comentários sobre os Pontos em Destaque**

---

# **ETL Pipeline com Tracing e Banco de Dados PostgreSQL**

Este projeto implementa um pipeline ETL (Extract, Transform, Load) com instrumentação de tracing usando **Logfire** e armazenamento em um banco de dados PostgreSQL remoto. O objetivo é demonstrar como integrar spans para monitorar o desempenho e acompanhar cada etapa do pipeline.

---

## **Destaques do Código**

### 1. **Tracing com Spans**
- O uso de spans no **Logfire** permite monitorar o tempo de execução de cada etapa do pipeline.
- Exemplos no código:
  - **Etapa de Extração**:
    ```python
    with logfire.span("Fazendo a requisição para obter o valor do Bitcoin"):
        response = requests.get(url=URL)
    ```
    - Este span mede o tempo para realizar a requisição HTTP.
  - **Etapa de Transformação**:
    ```python
    with logfire.span("Validando os dados com Pydantic"):
        validated_data = ApiResponse(**data)
    ```
    - Este span mede o tempo para validar os dados com o modelo **Pydantic**.
  - **Etapa de Carregamento**:
    ```python
    with logfire.span("Carregando os dados no banco de dados PostgreSQL"):
        session.add(bitcoin_entry)
        session.commit()
    ```
    - Este span mede o tempo para salvar os dados no banco PostgreSQL usando SQLAlchemy.

### 2. **Logs Detalhados**
- O **Logfire** é usado para gerar logs ricos com contexto adicional. Exemplos incluem:
  - Mensagem de sucesso na conexão:
    ```python
    logfire.info("Conexão bem-sucedida com o banco PostgreSQL.")
    ```
  - Dados inseridos no banco:
    ```python
    logfire.info(
        "Dado inserido no banco: {amount} {base}/{currency} em {timestamp}",
        amount=bitcoin_entry.amount,
        base=bitcoin_entry.base,
        currency=bitcoin_entry.currency,
        timestamp=bitcoin_entry.timestamp,
    )
    ```

### 3. **Monitoramento do Pipeline Completo**
- Um span envolve a execução completa do pipeline:
  ```python
  with logfire.span("Execução completa do pipeline ETL"):
      raw_data = extract()
      transformed_data = transform(raw_data)
      load(transformed_data)
  ```
  - Ele registra quanto tempo o pipeline completo leva para ser executado.

### 4. **Loop Contínuo**
- O pipeline é executado em um loop contínuo com uma pausa de 10 segundos entre as execuções:
  ```python
  while True:
      with logfire.span("Execução completa do pipeline ETL"):
          raw_data = extract()
          transformed_data = transform(raw_data)
          load(transformed_data)
          logfire.info("Pipeline concluído. Aguardando 10 segundos antes de repetir.")
      sleep(10)
  ```
- É possível interromper o loop pressionando `Ctrl+C`, capturado pelo seguinte bloco:
  ```python
  except KeyboardInterrupt:
      logfire.info("Execução do pipeline interrompida pelo usuário.")
  ```

---

## **Passos para Rodar o Projeto**

1. **Clonar o Repositório**
   ```bash
   git clone https://github.com/seu-repositorio/etl-pipeline-logfire.git
   cd etl-pipeline-logfire
   ```

2. **Configurar o Ambiente**
   - Certifique-se de que o Python 3.8+ está instalado.
   - Crie e ative um ambiente virtual:
     ```bash
     python -m venv .venv
     source .venv/bin/activate  # No Windows: .venv\Scripts\activate
     ```

3. **Instalar as Dependências**
   - Instale as bibliotecas necessárias:
     ```bash
     pip install requests sqlalchemy logfire pydantic psycopg2
     ```

4. **Configurar o Banco PostgreSQL**
   - Configure a URI do PostgreSQL no arquivo:
     ```python
     POSTGRES_URI = "postgresql://<USUARIO>:<SENHA>@<HOST>:<PORTA>/<BANCO>"
     ```
   - Certifique-se de que o banco de dados está acessível e o usuário tem permissões para criar tabelas.

5. **Executar o Script**
   - Rode o script:
     ```bash
     python main.py
     ```

6. **Parar o Pipeline**
   - Use `Ctrl+C` para interromper a execução do pipeline.

---

## **Exemplo de Saída**

### **Logs no Console**
Você verá logs detalhados para cada etapa:
```plaintext
Conexão bem-sucedida com o banco PostgreSQL.
[Span] Fazendo a requisição para obter o valor do Bitcoin
[Span] Validando os dados com Pydantic
[Span] Carregando os dados no banco de dados PostgreSQL
[Dado inserido no banco: 97231.45 BTC/USD em 2024-12-01 10:30:15]
[Pipeline concluído. Aguardando 10 segundos antes de repetir.]
```

---

## **Benefícios do Tracing e Logging**

1. **Monitoramento de Desempenho**:
   - Spans permitem identificar gargalos em cada etapa do pipeline.
   - Medições precisas do tempo de execução ajudam na otimização.

2. **Visibilidade do Sistema**:
   - Logs enriquecidos fornecem informações contextuais sobre o estado do pipeline.
   - Possibilidade de correlacionar eventos entre diferentes sistemas.

3. **Facilidade de Depuração**:
   - Mensagens detalhadas ajudam a diagnosticar problemas rapidamente.

4. **Manutenção e Escalabilidade**:
   - Tracing oferece uma visão clara do fluxo do sistema, facilitando a manutenção e escalabilidade.

---

Com este projeto, você tem uma base robusta para monitorar e otimizar pipelines ETL, além de integrar com ferramentas modernas de observabilidade como **Logfire**. 🚀