# Databricks notebook source
# Helper Functions
def get_table_name(schema, table):
    """Get table name"""
    return f"{catalog}.{schema}.{table}"

def get_storage_path(container, subdir):
    """Get ABFSS storage path"""
    container_name = containers.get(container, container)
    path = f"abfss://{container_name}@{storage_account}.dfs.core.windows.net"
    return f"{path}/{subdir}" if subdir else path

def get_checkpoint_path(table_name):
    """Get checkpoint path for streaming operations"""
    return get_storage_path("checkpoints", table_name)