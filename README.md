# TFL Analytics Pipeline — Data Warehouse and Analytics Project

## Description
`tfl-analytics-pipeline` is an end-to-end data engineering project that builds an analytics-ready data warehouse from Transport for London (TfL) operational data. It combines **Azure Data Factory (ADF)** for orchestration, **Infrastructure-as-Code (Bicep)** for repeatable deployments, and a **Medallion Architecture (Bronze → Silver → Gold)** transformation approach to produce curated datasets for reporting and analysis.

This repository is structured to support:
- Reproducible environments (IaC + parameterization)
- Automated ingestion and transformation pipelines
- Clear separation of raw, conformed, and curated data layers
- Basic validation and data quality checks

---

## 🏗️ Data Architecture

The data architecture for this project follows **Medallion Architecture** — **Bronze**, **Silver**, and **Gold** layers:

![Medallion Architecture - TfL Analytics Pipeline](https://github.com/MichaelOforgu/tfl-analytics-pipeline/blob/main/docs/data_architecture_tfl.png)

- **Bronze (Raw / Landing):** Source-aligned data ingested with minimal transformation. Retains fidelity to the source for traceability and reprocessing.
- **Silver (Clean / Conformed):** Cleansed and standardized datasets (types, schemas, deduplication, null handling, and business rules normalization).
- **Gold (Curated / Analytics):** Business-ready datasets optimized for consumption (facts/dimensions or analytics marts), designed for BI dashboards, KPI tracking, and ad-hoc queries.


## 📖 Project Overview

This project involves:

- **Orchestration with Azure Data Factory (ADF)**  
  Pipelines, datasets, linked services, and factory resources are versioned under `adf/` to support collaboration and CI/CD-style deployments.

- **Infrastructure-as-Code (Bicep)**  
  Azure resources are defined and deployed via Bicep templates under `infrastructure/`, enabling consistent provisioning across environments (e.g., dev/test/prod).

- **Layered transformations (Bronze/Silver/Gold)**  
  Transformation logic is organized under `src/` by data layer, promoting clear ownership and maintainability.

- **Configuration-driven execution**  
  Centralized configuration via `config/config.yaml` to support environment settings, source definitions, and pipeline parameters.

- **Data quality and transformation validation**  
  Validation notebooks under `test/` provide checks for data quality and transformation correctness.

---

## 🚀 Project Requirements

### Objective
Design and implement a production-style analytics pipeline that ingests TfL data, applies standardized transformations, and publishes curated datasets for downstream analytics.

### Specifications
- **Ingestion (Bronze)**
  - Ingest source data via ADF pipelines.
  - Persist raw/landing data with strong traceability (source + load timestamps, run identifiers where applicable).
  - Ensure ingestion can be re-run safely (idempotency where possible).

- **Conformance (Silver)**
  - Standardize schema, data types, and formats.
  - Apply deduplication, null handling, and basic validation rules.
  - Track data quality issues (failed checks, anomaly counts, etc.) where feasible.

- **Curation (Gold)**
  - Publish analytics-ready datasets (e.g., marts, facts/dimensions, or wide reporting tables).
  - Optimize for consumption by BI tools and stakeholders.

- **Deployment & Environment Management**
  - Provision Azure resources via Bicep templates.
  - Parameterize deployments for multiple environments.

- **Testing**
  - Provide transformation and quality validation artifacts (initially via notebooks; ideally expandable to automated test execution).

---

## 📂 Repository Structure

```text
tfl-analytics-pipeline/
├─ adf/                          # Azure Data Factory assets
│  ├─ dataset/                   # ADF datasets
│  ├─ factory/                   # ADF factory definition
│  ├─ linkedService/             # ADF linked services (connections)
│  └─ pipeline/                  # ADF pipelines (orchestration)
│
├─ config/
│  └─ config.yaml                # Central configuration for the pipeline
│
├─ docs/                         # Documentation (add architecture diagrams, runbooks)
│  └─ data_architecture_tfl      # Data architecture
│
├─ infrastructure/               # IaC and deployment automation
│  ├─ bicep/                     # Bicep templates
│  ├─ parameters/                # Environment parameter files
│  └─ deploy.sh                  # Deployment script
│
├─ src/                          # Transformation code by medallion layer
│  ├─ bronze/                    # Raw ingestion/landing transformations
│  ├─ silver/                    # Cleansing + conformance transformations
│  ├─ gold/                      # Curated analytics models
│  ├─ common/                    # Shared logic used across layers
│  └─ utils/                     # Helpers/utilities
│
├─ test/                         # Validation artifacts
│  ├─ test_data_quality.ipynb     # Data quality validation notebook
│  └─ test_transformations.ipynb  # Transformation validation notebook
│
├─ requirements.txt              # Python dependencies
├─ .gitignore
└─ README.md
```

---


## Testing & Validation
Validation notebooks are available under `test/`:
- `test_data_quality.ipynb` — sanity checks and data quality assertions
- `test_transformations.ipynb` — validation of transformation outputs

For an industry-standard next step, consider converting these checks into:
- Automated unit tests (e.g., `pytest`)
- Data quality framework checks (e.g., Great Expectations)
- CI integration (GitHub Actions) for repeatable verification

---
