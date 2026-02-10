# Databricks notebook source
# MAGIC %run ../config/load_config

# COMMAND ----------

# Verify external location exists
print(f"\nChecking external locations")
spark.sql("SHOW EXTERNAL LOCATIONS").show()

# Create catalog
spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog} COMMENT 'TFL Analytics Pipeline catalog for {env} environment'")
print(f"\n✅ Catalog '{catalog}' created")

# Create landing, bronze, silver and gold schemas
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.landing")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.bronze")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.silver")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.gold")
print(f"✅ Schemas created: landing, bronze, silver, gold")

# Create external volume pointing to landing container
landing_path = get_storage_path("landing","")
spark.sql(f"CREATE EXTERNAL VOLUME IF NOT EXISTS {catalog}.landing.tfl_raw LOCATION '{landing_path}'")
print(f"✅ External volume created: {catalog}.landing.tfl_raw")
print(f"   Location: {landing_path}")

# Verification
print("\n" + "="*70)
print(f"SETUP COMPLETE - {env.upper()} ENVIRONMENT")
print("="*70)

spark.sql(f"SHOW SCHEMAS IN {catalog}").show(truncate=False)
print(f"\n✅ Ready for data ingestion!")