# TfL Analytics Pipeline

A cloud-based data analytics pipeline for ingesting, transforming, and analyzing Transport for London (TfL) real-time data using Azure Data Factory, Databricks, and the Medallion architecture.

## Overview

This project implements an end-to-end data pipeline that:
- Ingests real-time data from the TfL API (bus arrivals, line status, stop points, London boroughs)
- Processes data through a three-tier medallion architecture (Bronze → Silver → Gold)
- Provides analytics-ready datasets for business intelligence and reporting
- Uses infrastructure-as-code (Bicep) for reproducible Azure deployments

## Architecture

### Technologies
- **Azure Data Factory (ADF)**: Orchestrates data ingestion from TfL API to Azure Data Lake Storage (ADLS)
- **Azure Data Lake Storage Gen2**: Stores raw and processed data in hierarchical layers
- **Azure Databricks**: Processes and transforms data through the medallion architecture
- **Bicep/ARM Templates**: Infrastructure as Code for resource provisioning

### Medallion Architecture

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/b1c720d8-39d3-45d3-aa43-fa6499c9463f" />

```
TfL API → ADF → Landing → Bronze → Silver → Gold
                 (Raw)    (Clean)  (Enriched) (Aggregated)
```

**Bronze Layer**: Raw data ingestion from landing zone
- `ingest_bus_arrivals.ipynb`
- `ingest_line_status.ipynb`
- `ingest_stop_points.ipynb`
- `ingest_london_boroughs.ipynb`

**Silver Layer**: Data cleaning, transformation, and enrichment
- `transform_bus_arrivals.ipynb`
- `transform_line_status.ipynb`
- `transform_stop_points.ipynb`
- `transform_london_boroughs.ipynb`
- `enrich_stops_with_borough.ipynb`
- `enrich_arrival_events.ipynb`

**Gold Layer**: Business-level aggregations and KPIs
- `arrival_performance_kpi.ipynb`

## Prerequisites

- **Azure Subscription** with appropriate permissions
- **Azure CLI** installed and configured
- **Databricks workspace** (deployed via Bicep)
- **TfL API credentials** (if required for specific endpoints)
- **Python 3.x** (for local development)

## Project Structure

```
tfl-analytics-pipeline/
├── adf/                          # Azure Data Factory artifacts
│   ├── dataset/                  # Dataset definitions
│   ├── factory/                  # Factory configuration
│   ├── linkedService/            # Linked service connections
│   └── pipeline/                 # Pipeline definitions
│       ├── pl_ingest_tfl_arrivals_hourly.json
│       ├── pl_ingest_tfl_line_and_stops_daily.json
│       ├── pl_error_handler.json
│       └── exec_pl_tfl_to_landing_ingest.json
├── databricks/                   # Databricks notebooks
│   ├── bronze/                   # Bronze layer ingestion
│   │   ├── 00_bronze_orchestrator.ipynb
│   │   └── ingest_*.ipynb
│   ├── silver/                   # Silver layer transformations
│   │   ├── 00_silver_orchestrator.ipynb
│   │   ├── transform_*.ipynb
│   │   └── enrich_*.ipynb
│   ├── gold/                     # Gold layer aggregations
│   │   ├── 00_gold_orchestrator.ipynb
│   │   └── arrival_performance_kpi.ipynb
│   ├── config/                   # Configuration files
│   │   ├── config.yaml
│   │   └── load_config.ipynb
│   ├── common/                   # Shared utilities
│   ├── setup/                    # Setup scripts
│   └── test/                     # Test notebooks
├── infrastructure/               # Infrastructure as Code
│   ├── bicep/                    # Bicep templates
│   │   ├── main.bicep           # Main deployment template
│   │   └── resources.bicep      # Resource definitions
│   ├── parameters/               # Environment parameters
│   └── deploy.sh                # Deployment script
└── requirements.txt              # Python dependencies
```

## Setup and Deployment

### 1. Infrastructure Deployment

Deploy the Azure infrastructure using Bicep:

```bash
# Login to Azure
az login

# Deploy to development environment
az deployment sub create \
    --location uksouth \
    --template-file ./infrastructure/bicep/main.bicep \
    --parameters ./infrastructure/parameters/dev.parameters.json
```

This creates:
- Resource Group
- Azure Data Lake Storage Gen2 (with landing, bronze, silver, gold containers)
- Azure Data Factory
- Azure Databricks Workspace
- Databricks Access Connector

### 2. Configuration

Update the configuration file for your environment:

**`databricks/config/config.yaml`**
- Set catalog names (dev/prod)
- Configure schema names (bronze, silver, gold)
- Update storage account names
- Configure external locations and credentials

### 3. Databricks Setup

1. Upload notebooks to your Databricks workspace:
   - Bronze layer: `databricks/bronze/`
   - Silver layer: `databricks/silver/`
   - Gold layer: `databricks/gold/`
   - Configuration: `databricks/config/`

2. Create Unity Catalog resources:
   - Catalogs: `tfl_dev`, `tfl_prod`
   - Schemas: `bronze`, `silver`, `gold`
   - External locations for ADLS containers
   - Storage credentials

3. Configure cluster with required libraries

### 4. Azure Data Factory Setup

Import ADF artifacts into your Data Factory:
- Linked Services (configure connection strings and credentials)
- Datasets
- Pipelines

## Running the Pipeline

### Manual Execution

**Bronze Layer (Data Ingestion)**
```python
# Run in Databricks
%run databricks/bronze/00_bronze_orchestrator
```

**Silver Layer (Transformations)**
```python
# Run in Databricks
%run databricks/silver/00_silver_orchestrator
```

**Gold Layer (Aggregations)**
```python
# Run in Databricks
%run databricks/gold/00_gold_orchestrator
```

### Scheduled Execution

Configure ADF pipeline triggers:
- **Hourly**: `pl_ingest_tfl_arrivals_hourly.json` - Ingests bus arrival data
- **Daily**: `pl_ingest_tfl_line_and_stops_daily.json` - Ingests line status and stop points

## Data Sources

The pipeline integrates with Transport for London (TfL) Unified API:
- **Bus Arrivals**: Real-time bus arrival predictions
- **Line Status**: Current status of transport lines
- **Stop Points**: Bus stop locations and metadata
- **London Boroughs**: Geographic boundary data for London boroughs

API Documentation: https://api.tfl.gov.uk/

### Testing

Run test notebooks in `databricks/test/` to validate transformations and data quality.

## Data Flow

1. **Ingestion (ADF)**: TfL API → ADLS Landing Zone (JSON files)
2. **Bronze (Databricks)**: Landing → Bronze tables (raw data, schema-on-read)
3. **Silver (Databricks)**: Bronze → Silver tables (cleaned, standardized, enriched)
4. **Gold (Databricks)**: Silver → Gold tables (aggregated KPIs, business metrics)

## Environments

- **Development (`dev`)**: For development and testing
- **Production (`prod`)**: For production workloads

Environment-specific configurations are maintained in:
- `config.yaml`
- `infrastructure/parameters/`


## Acknowledgments

Data provided by Transport for London (TfL) Unified API.
