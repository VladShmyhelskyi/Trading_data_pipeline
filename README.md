# 📈 Enterprise Trading Data Pipeline & Medallion Architecture

[![Trading Pipeline CI](https://github.com/VladShmyhelskyi/Trading_data_pipeline/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/VladShmyhelskyi/Trading_data_pipeline/actions/workflows/ci.yml)

A production-grade, end-to-end Data Engineering pipeline designed to ingest, transform, and aggregate financial market data using a **Medallion Architecture (Bronze/Silver/Gold)**, integrating local Big Data processing with **Apache Spark (PySpark)** and cloud data warehousing via **Snowflake**.

---

## 🌟 Key Features

- **Automated Data Ingestion (Bronze Layer):** Automated extraction and staging of raw financial market data in real time using `yfinance`.
- **Distributed Data Processing (Silver Layer):** Fast and reliable distributed data cleaning, deduplication, and transformation powered by Apache Spark (PySpark), including derived financial metrics calculation.
- **Multi-Format Export & Cloud Warehousing (Gold Layer):** Support for exporting processed datasets to local columnar and tabular formats (`Parquet`, `CSV`) alongside seamless integration with Snowflake Cloud Data Warehouse.

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

## 📊 Business Intelligence & Visualization (Power BI)

The Gold analytical layer (`processed_market_data.csv`) is visualized in **Microsoft Power BI Desktop** (`powerbi/eurusd_dashboard.pbix`) to provide an executive overview of `EURUSD=X` price action and daily volatility.

![Power BI Market Dashboard](assets/powerbi_dashboard.png)

### Key Dashboard Features:
- **Executive KPI Header:** Tracks `Latest Close`, `Period High`, `Period Low`, `Avg Close`, and `Period Return %` using custom **DAX** time-intelligence measures (`FIRSTDATE`, `LASTDATE`, `CALCULATE`, `DIVIDE`).
- **Price Trend Dynamics:** Interactive area chart illustrating closing price movements across the reporting period with a calibrated Y-axis scale.
- **Volatility Analysis:** Clustered column chart of `price_change` enhanced with rule-based conditional formatting (green for positive daily gains, red for pullbacks).
- **Granular OHLC Inspection:** Formatted data table displaying chronological daily quotes (`open`, `high`, `low`, `close`, `price_change`) to 4-decimal precision without distorted column totals.