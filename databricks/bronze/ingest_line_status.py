# Databricks notebook source
# MAGIC %run ../config/load_config

# COMMAND ----------

from pyspark.sql import functions as F

# Define base volume and paths for raw data, checkpoints, and schema evolution
source_subdir="lines",
target_table="lines_bz"

raw_volume_path = f"/Volumes/{catalog}/landing/tfl_raw"
bronze_checkpoint = get_storage_path("checkpoints", f"bronze/{target_table}")
schema_path = get_storage_path("checkpoints", f"schema/{target_table}")

def ingest_line_status(once=True, processing_time="5 seconds"):
    # Read raw stream data into a dataframe using Autoloader
    df_stream = (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("cloudFiles.inferColumnTypes", "true")
            .option("cloudFiles.schemaLocation", schema_path)
            .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
            .option("recursiveFileLookup", "true")
            .option("maxFilesPerTrigger", 1)
            .load(f"{raw_volume_path}/{source_subdir}")
            .withColumn("_ingest_time", F.current_timestamp())  # Add ingestion timestamp
            .withColumn("_source_file", F.input_file_name())    # Add source file name
    )

    # Write streaming data to delta table
    stream_writer = (
        df_stream.writeStream
            .format("delta")
            .outputMode("append")
            .option("checkpointLocation", bronze_checkpoint)
            .queryName(target_table)
    )

    # Trigger streaming write either once or continuously
    if once:
        stream_writer.trigger(availableNow=True).toTable(f"{catalog}.{schema_bronze}.{target_table}")
    else:
        stream_writer.trigger(processingTime=processing_time).toTable(f"{catalog}.{schema_bronze}.{target_table}")

    
ingest_line_status(once=True, processing_time="5 seconds")