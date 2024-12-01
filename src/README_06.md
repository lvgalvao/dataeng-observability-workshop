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

Aqui está uma query otimizada com apenas os campos necessários para monitorar o comportamento da etapa `load` no pipeline e como interpretar os resultados para identificar tendências de aumento no tempo de execução:

### Query Otimizada
```sql
SELECT
    start_timestamp,
    histogram_min AS min_duration_ms,
    histogram_max AS max_duration_ms,
    histogram_sum AS total_duration_ms,
    histogram_count,
    (histogram_sum / histogram_count) AS avg_duration_ms
FROM metrics
WHERE metric_name = 'stage_duration' AND attributes->>'stage' = 'load'
ORDER BY start_timestamp DESC;
```

---

### Explicação dos Campos Selecionados

1. **start_timestamp**  
   - **Descrição:** Indica o momento em que a coleta do histograma começou.  
   - **Uso:** Permite analisar a evolução ao longo do tempo.

2. **histogram_min (min_duration_ms)**  
   - **Descrição:** Menor tempo de execução registrado no intervalo.  
   - **Uso:** Ajuda a identificar se o mínimo também está aumentando ao longo do tempo.

3. **histogram_max (max_duration_ms)**  
   - **Descrição:** Maior tempo de execução registrado no intervalo.  
   - **Uso:** Permite verificar picos de tempo de execução.

4. **histogram_sum (total_duration_ms)**  
   - **Descrição:** Soma total de todas as durações registradas no intervalo.  
   - **Uso:** Indica o acúmulo de tempo gasto na etapa `load`.

5. **histogram_count**  
   - **Descrição:** Número total de execuções registradas no intervalo.  
   - **Uso:** Essencial para calcular a média.

6. **avg_duration_ms**  
   - **Descrição:** Duração média de execução calculada como `histogram_sum / histogram_count`.  
   - **Uso:** A principal métrica para identificar tendências de aumento no tempo médio.

---

### Identificando Tendências de Aumento

Para identificar se o tempo de execução da etapa `load` está subindo, você deve observar:

1. **Aumento do Tempo Médio (`avg_duration_ms`)**  
   - Ordene os resultados pelo `start_timestamp` para visualizar a evolução temporal.  
   - Um crescimento consistente ou súbito no tempo médio (`avg_duration_ms`) indica que a execução da etapa está ficando mais lenta.

   **Exemplo:**  
   ```
   start_timestamp       avg_duration_ms
   2024-12-01 11:00:00   450
   2024-12-01 11:10:00   470
   2024-12-01 11:20:00   490
   ```

2. **Aumento no Tempo Máximo (`max_duration_ms`)**  
   - Verifique se os valores de `histogram_max` estão crescendo.  
   - Picos mais altos sugerem que algumas execuções estão enfrentando maior latência.

3. **Comparação do Tempo Mínimo (`min_duration_ms`)**  
   - Se o tempo mínimo também subir, isso pode indicar um problema geral afetando todas as execuções, e não apenas exceções.

4. **Aumento no `histogram_sum`**  
   - Se a soma total (`histogram_sum`) aumenta sem um aumento correspondente em `histogram_count`, isso sugere que os tempos de execução individuais estão aumentando.

---

### Visualizando no Gráfico
Você pode criar um gráfico de linhas com:
- **Eixo X:** `start_timestamp` (tempo)  
- **Eixo Y:** `avg_duration_ms` (tempo médio)  

Esse gráfico mostrará claramente se o tempo médio de execução está subindo ao longo do tempo. Adicionalmente, inclua linhas para `min_duration_ms` e `max_duration_ms` para observar picos e variações.

```sql
SELECT
    start_timestamp,
    histogram_min AS min_duration_ms,
    histogram_max AS max_duration_ms,
    histogram_sum AS total_duration_ms,
    histogram_count,
    (histogram_sum / histogram_count) AS avg_duration_ms
FROM metrics
WHERE metric_name = 'stage_duration' AND attributes->>'stage' = 'load' and histogram_count = 6
ORDER BY start_timestamp ASC;
```sql