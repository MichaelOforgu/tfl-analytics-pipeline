# Databricks notebook source
# MAGIC %run ../config/load_config

# COMMAND ----------

import time

NOTEBOOKS = [
    "ingest_bus_arrivals",
    "ingest_line_status",
    "ingest_stop_points",
    "ingest_london_boroughs"
]

print("\nStarting bronze layer consumption...")
start = time.time()

for nb in NOTEBOOKS:
    print(f"\n▶ Running: {nb}")
    dbutils.notebook.run(nb, timeout_seconds=3600)
    print(f"  ✓ Completed")

print(f"\n✓ Total time: {time.time() - start:.2f}s")

## Validate Bronze Tables
TABLES = ["arrivals_bz", "lines_bz", "stops_bz", "boroughs_bz"]

print("\nValidating bronze layer records...")
for table in TABLES:
    full_table = get_table_name(schema_bronze, table)
    count = spark.table(full_table).count()
    assert count > 0, f"{table} is empty"
    print(f"✓ {table}: {count:,} records")