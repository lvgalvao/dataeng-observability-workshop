from google.cloud import bigquery

import logfire

logfire.configure()

client = bigquery.Client()
query = """
SELECT name
FROM `bigquery-public-data.usa_names.usa_1910_2013`
WHERE state = "TX"
LIMIT 100
"""
query_job = client.query(query)
print(list(query_job.result()))