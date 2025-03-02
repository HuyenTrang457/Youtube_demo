# YouTube Ratings ETL Pipeline

This project implements a comprehensive ETL (Extract, Transform, Load) pipeline for processing YouTube trending videos data across multiple regions. The pipeline follows a medallion architecture with Bronze, Silver, and Gold layers to transform raw data into analytics-ready datasets.

## Architecture Overview

![ETL Pipeline Architecture](https://miro.medium.com/v2/resize:fit:1400/1*hkqRLTJVrWJsJUJlqyZiHQ.png)

### Data Flow Process

1. **Bronze Layer (Raw Data Extraction)**
   - **Purpose**: Capture raw data exactly as it appears in source systems
   - **Process**: 
     - Extract raw data from MySQL database tables (10 regional tables)
     - Store data in MinIO data lake in Parquet format with minimal processing
     - Preserve original data structure, values, and relationships
     - Add extraction timestamp metadata for lineage tracking
   - **Output**: Raw, immutable data snapshots partitioned by region and date

2. **Silver Layer (Data Cleaning & Standardization)**
   - **Purpose**: Transform raw data into clean, validated, and standardized formats
   - **Process**:
     - Clean text fields (trim whitespace, standardize case)
     - Handle missing values and convert to appropriate data types
     - Standardize timestamps across all regions
     - Remove duplicates and invalid records
     - Add derived metrics (engagement rate, like ratio)
     - Parse complex fields (tags into lists)
   - **Output**: Validated, consistent datasets ready for analytical modeling

3. **Gold Layer (Analytics-Ready Data)**
   - **Purpose**: Structure data for specific business use cases and analytics
   - **Process**:
     - Create dimensional model with star schema:
       - Dimension tables: videos, channels, categories, regions
       - Fact tables: trending_videos with metrics
     - Generate pre-aggregated tables for common analytics patterns
     - Apply business rules and calculations
     - Optimize for query performance
   - **Output**: Analytics-ready tables in PostgreSQL for Data Science and ML applications

## Components & Technologies

- **Data Sources**: MySQL database with regional YouTube trending data
- **Data Lake**: MinIO object storage (S3-compatible)
- **Data Warehouse**: PostgreSQL database
- **Orchestration**: Dagster workflow management
- **Transformation**: Pandas (Python) and DBT (SQL)
- **Infrastructure**: Docker containerization

## Project Structure

```
etl_pipeline/
│── assets/                # Dagster assets for each layer
│   │── bronze_layer.py    # Extract data from MySQL to MinIO
│   │── silver_layer.py    # Clean and process data
│   │── gold_layer.py      # Create analytics tables
│
│── resources/             # IO managers for different data sources
│   │── mysql_io_manager.py
│   │── minio_io_manager.py
│   │── psql_io_manager.py
│
│── dbt/                   # DBT models for transformations
│   │── models/
│   │── snapshots/
│   │── macros/
│
│── docker/                # Docker configuration
│
│── config/                # Configuration files
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.10+

### Setup

1. Clone the repository
2. Build and start the containers:

```bash
docker-compose up -d
```

3. Access the Dagster UI at http://localhost:3000

### Running the Pipeline

The pipeline is scheduled to run automatically with the following cadence:

| Layer   | Schedule        | Description                                |
|---------|----------------|--------------------------------------------|
| Bronze  | Every 6 hours   | Extract raw data from source systems       |
| Silver  | 30 min after Bronze | Process and clean the extracted data   |
| Gold    | Every 12 hours  | Transform clean data into analytics models |

You can also trigger the pipeline manually through the Dagster UI for testing or ad-hoc runs.

## Data Model

### Bronze Layer Tables
- `bronze_trending_videos`: Raw trending videos data from all regions
- `bronze_video_categories`: Raw video categories data

### Silver Layer Tables
- `silver_trending_videos`: Cleaned trending videos with standardized fields and derived metrics
- `silver_video_categories`: Cleaned and deduplicated video categories

### Gold Layer Tables
- **Dimension Tables**:
  - `dim_videos`: Unique videos with attributes
  - `dim_channels`: Unique channels
  - `dim_categories`: Video categories
  - `dim_regions`: Geographic regions
- **Fact Tables**:
  - `fact_trending_videos`: Trending video metrics with foreign keys to dimensions
- **Aggregated Tables**:
  - `agg_region_trends`: Metrics aggregated by region
  - `agg_category_performance`: Metrics aggregated by video category

## Applications

This data pipeline supports various analytical use cases:

- **Data Science (DS)**:
  - Analysis of trending video patterns across regions
  - Content performance comparison by category
  - Temporal trend analysis

- **Machine Learning (ML)**:
  - Prediction of video engagement based on attributes
  - Content recommendation systems
  - Anomaly detection for viral content

## Monitoring and Maintenance

- Pipeline execution logs are available in the Dagster UI
- Each layer includes metadata tracking for data lineage
- Tests are provided for each layer to ensure data quality