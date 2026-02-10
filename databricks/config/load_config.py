# Databricks notebook source
"""
Configuration Loader for TFL Analytics Pipeline
Loads environment-specific configuration and provides helper functions
"""

import json
import os
from typing import Dict, Any

def get_environment():
    """Get current environment from environment variable"""
    return os.getenv('ENVIRONMENT', 'dev')

def load_config_from_file(env):
    """Load configuration from JSON file"""
    config_path = "/Workspace/Users/@chukwukaoforgugmail.onmicrosoft.com/tfl-analytics-pipeline/databricks/config/env-config.json"
    
    with open(config_path, "r") as f:
        all_configs = json.load(f)
    
    if env not in all_configs:
        raise ValueError(
            f"Environment '{env}' not found in config. "
            f"Available: {list(all_configs.keys())}"
        )
    
    return all_configs[env]

# Load configuration
env = get_environment()
config = load_config_from_file(env)

# Extract catalog and schema values
catalog = config["catalog"]
schema_bronze = config["schemas"]["bronze"]
schema_silver = config["schemas"]["silver"]
schema_gold = config["schemas"]["gold"]

storage_account = config["storage"]["account_name"]
storage_credential = config["storage"]["storage_credential"]

# External locations
external_locations = config["storage"]["external_locations"]
ext_loc_landing = external_locations["landing"]
ext_loc_bronze = external_locations["bronze"]
ext_loc_silver = external_locations["silver"]
ext_loc_gold = external_locations["gold"]

# Containers
containers = config["storage"]["containers"]
container_landing = containers["landing"]
container_bronze = containers["bronze"]
container_silver = containers["silver"]
container_gold = containers["gold"]
container_checkpoints = containers["checkpoints"]

# COMMAND ----------

# MAGIC %run ../common/catalog_utils