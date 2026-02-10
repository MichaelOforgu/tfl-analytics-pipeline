# Databricks notebook source
# Create widget for environment selection
dbutils.widgets.dropdown("env", "dev", ["dev", "prod"])
env = dbutils.widgets.get("env")

# COMMAND ----------

import json

# Load config
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
repo_root = "/".join(notebook_path.split("/")[:5]) 
config_path = f"/Workspace{repo_root}/config/env-config.json"

with open(config_path, "r") as f:
    config = json.load(f)[env]

# Extract values
storage_config = config["storage"]
databricks_config = config["databricks"]

catalog_name = databricks_config["catalog_name"]
storage_account = storage_config["account_name"]
storage_credential = databricks_config["storage_credential"]

# Build storage locations
landing_location = f"abfss://{storage_config['container_landing']}@{storage_account}.dfs.core.windows.net/"
bronze_location = f"abfss://{storage_config['container_bronze']}@{storage_account}.dfs.core.windows.net/"
silver_location = f"abfss://{storage_config['container_silver']}@{storage_account}.dfs.core.windows.net/"
gold_location = f"abfss://{storage_config['container_gold']}@{storage_account}.dfs.core.windows.net/"
checkpoints_location = f"abfss://{storage_config['container_checkpoints']}@{storage_account}.dfs.core.windows.net/"

print(f"✅ Configuration loaded:")
print(f"Storage Account: {st_account_name}")
print(f"Catalog: {catalog_name}")


# Verify storage credential exists
print(f"\nChecking storage credential")
spark.sql(f"DESCRIBE STORAGE CREDENTIAL {storage_credential}").show()

# Verify external location exists
print(f"\nChecking external locations")
spark.sql("SHOW EXTERNAL LOCATIONS").show()

# Create catalog
spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog_name} COMMENT 'TFL Analytics Pipeline catalog for {env} environment'")
print(f"\n✅ Catalog '{catalog_name}' created")

# Use the catalog
spark.sql(f"USE CATALOG {catalog_name}")

# Create schemas
spark.sql(f"CREATE SCHEMA IF NOT EXISTS landing LOCATION '{landing_location}'")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS bronze MANAGED LOCATION '{bronze_location}'")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS silver MANAGED LOCATION '{silver_location}'")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS gold LOCATION '{gold_location}'")
print(f"✅ Schemas created: landing, bronze, silver, gold")

# Create EXTERNAL volume pointing to landing container
spark.sql(f"CREATE EXTERNAL VOLUME IF NOT EXISTS {catalog_name}.landing.tfl_raw LOCATION '{landing_location}'")
print(f"✅ External volume created: {catalog_name}.landing.tfl_raw")
print(f"   Location: {landing_location}")

# Verification
print("\n" + "="*70)
print(f"SETUP COMPLETE - {env.upper()} ENVIRONMENT")
print("="*70)

spark.sql(f"SHOW SCHEMAS IN {catalog_name}").show(truncate=False)
print(f"\n✅ Ready for data ingestion!")

# COMMAND ----------

