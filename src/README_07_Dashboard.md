# **README - Monitoramento de Métricas no Pipeline ETL**

Este projeto utiliza **Logfire** para monitorar e registrar métricas de desempenho de um pipeline ETL que realiza extração de dados de uma API, transformação e carga em um banco de dados PostgreSQL. A única métrica monitorada atualmente é **`stage_duration`**, que mede o tempo de execução de cada etapa do pipeline.

---

## **Métrica Monitorada**

### 1. **`stage_duration`**
- **Descrição:** Mede o tempo de execução em milissegundos para cada etapa do pipeline ETL.
- **Etapas monitoradas:**
  - **Extract:** Requisição à API para obter o valor do Bitcoin.
  - **Transform:** Validação dos dados recebidos usando o Pydantic.
  - **Load:** Inserção dos dados validados no banco de dados PostgreSQL.
- **Tipo:** `Histogram` (histograma exponencial).
- **Unidade:** Milissegundos (ms).
- **Atributos:**
  - `stage`: Nome da etapa (e.g., "extract", "transform", "load").

---

## **Consultas SQL para Métricas**

### 1. **Resumo Estatístico por Etapa**

**Objetivo:** Obter a duração mínima, máxima, média e soma para cada etapa do pipeline ETL.

```sql
SELECT
    attributes->>'stage' AS stage,
    MIN(histogram_min) AS min_duration_ms,
    MAX(histogram_max) AS max_duration_ms,
    AVG(histogram_sum / histogram_count) AS avg_duration_ms,
    SUM(histogram_sum) AS total_duration_ms
FROM metrics
WHERE metric_name = 'stage_duration'
GROUP BY attributes->>'stage';
```

---

### 2. **Resumo Diário por Etapa**

**Objetivo:** Agregar estatísticas diárias para cada etapa.

```sql
SELECT
    day,
    attributes->>'stage' AS stage,
    COUNT(*) AS total_records,
    MIN(histogram_min) AS min_duration_ms,
    MAX(histogram_max) AS max_duration_ms,
    AVG(histogram_sum / histogram_count) AS avg_duration_ms,
    SUM(histogram_sum) AS total_duration_ms
FROM metrics
WHERE metric_name = 'stage_duration'
GROUP BY day, attributes->>'stage';
```

---

## **Instruções para Uso**

### Requisitos
- **Python:** 3.8+
- **Banco de Dados:** PostgreSQL
- **Dependências:**
  - `logfire`
  - `requests`
  - `pydantic`
  - `sqlalchemy`

### Executar o Pipeline
1. Configure a variável `POSTGRES_URI` com a URI do banco PostgreSQL.
2. Execute o script Python para iniciar o pipeline.
3. Os dados da métrica `stage_duration` serão enviados automaticamente ao Logfire.

---

## **Contribuição**

Se deseja contribuir, sinta-se à vontade para:
- Adicionar novas métricas ao pipeline.
- Propor melhorias nas consultas SQL.
- Melhorar a documentação.

---

## **Contato**
- Desenvolvedor: **Luciano Vasconcelos**
- E-mail: [luciano@example.com](mailto:luciano@example.com)

---

Este projeto é mantido com o objetivo de demonstrar boas práticas de monitoramento de métricas em pipelines ETL.