# 📈 Enterprise Trading Data Pipeline & Medallion Architecture

[![Trading Pipeline CI](https://github.com/VladShmyhelskyi/Trading_data_pipeline/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/VladShmyhelskyi/Trading_data_pipeline/actions/workflows/ci.yml)

A production-grade, end-to-end Data Engineering pipeline designed to ingest, transform, and aggregate financial market data using a **Medallion Architecture (Bronze/Silver/Gold)**, integrating local Big Data processing with **Apache Spark (PySpark)** and cloud data warehousing via **Snowflake**.

---

## 🌟 Key Features

* **Функція 1.** Автоматизоване завантаження та стажування сирих ринкових даних у режимі реального часу (`Bronze Layer`) за допомогою `yfinance`[cite: 1].
* **Функція 2.** Швидка та надійна розподілена очищення, дедуплікація й трансформація даних через Apache Spark (`Silver Layer`) з розрахунком додаткових показників[cite: 1].
* **Функція 3.** Підтримка експорту оброблених даних у локальні формати (`Parquet`, `CSV`) та інтеграція з хмарним сховищем Snowflake (`Gold Layer`)[cite: 1].

---

## 🏗️ Architecture & Data Flow

```text
[ Yahoo Finance API ] 
         │
         ▼
    (Bronze Layer) ──> Raw Ingestion & Multi-Ticker Staging
         │
         ▼
    (Silver Layer) ──> Distributed Cleansing, Deduplication & Enrichment (PySpark)
         │
         ▼
    (Gold Layer)   ──> Aggregated Financial Marts & Analytical Views (Snowflake)
```

## 🛠️ Tech Stack
```text
Core Language: Python 3.10+

Big Data Processing: Apache Spark (pyspark), Apache Arrow (pyarrow)

Cloud Data Warehouse: Snowflake (TRADING_WH, TRADING_DWH)

Market Data Source: yfinance API

Orchestration & Version Control: Git, GitHub Actions (CI/CD)

Environment Management: python-dotenv, venv
```

## Project Structure
``` text
Trading_data_pipeline/
│
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated CI/CD pipeline configuration
├── data/                        # Local storage for processed datasets (Parquet/CSV)
├── sql/                         # SQL scripts for DB initialization & Medallion transformations
│   ├── 00_basic_db.sql
│   ├── 01_init_db.sql
│   ├── 02_silver_transform.sql
│   └── 03_gold_transform.sql
├── src/                         # Core Python modules
│   ├── ingest_to_bronze.py      # Raw data ingestion
│   ├── spark_processor.py       # PySpark distributed transformations
│   ├── transform_silver.py      # Silver layer processing logic
│   └── transform_gold.py        # Gold layer aggregation
├── .env.example                 # Template for environment variables
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```