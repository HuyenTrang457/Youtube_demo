# YouTube Ratings ETL Pipeline - Process Guide

This document outlines the step-by-step process for setting up and running the YouTube Ratings ETL Pipeline.

## Initial Setup Process

1. **Environment Setup**
   - Clone the repository
   - Install Docker and Docker Compose
   - Build and start the containers: `docker-compose up -d`
   - This will start MySQL, PostgreSQL, MinIO, and Dagster services

2. **Data Loading Process**
   - Place the 10 CSV files in a directory:
     - CAvideos.csv (Canada)
     - DEvideos.csv (Germany)
     - FRvideos.csv (France)
     - GBvideos.csv (Great Britain)
     - INvideos.csv (India)
     - JPvideos.csv (Japan)
     - MXvideos.csv (Mexico)
     - RUvideos.csv (Russia)
     - USvideos.csv (United States)
     - NVideos.csv (Netherlands)
   - Run the data loading script: `python load_csv_data.py --csv-dir /path/to/csv/files`
   - This script will:
     - Connect to the MySQL database
     - Load each CSV file into its corresponding table
     - Convert all numeric fields to integer data types
     - Log the number of rows loaded for each region

3. **Pipeline Execution Process**
   - Access the Dagster UI at http://localhost:3000
   - Alternatively, run the pipeline from the command line:
     - Full pipeline: `python run_pipeline.py --layer all`
     - Bronze layer only: `python run_pipeline.py --layer bronze`
     - Silver layer only: `python run_pipeline.py --layer silver`
     - Gold layer only: `python run_pipeline.py --layer gold`

## Data Processing Flow

### 1. Bronze Layer (Raw Data Extraction)
   - **Input**: MySQL tables with raw CSV data
   - **Process**:
     - Extract data from all 10 regional tables
     - Add extraction timestamp and region metadata
     - Store in MinIO data lake as Parquet files
   - **Output**: `bronze_trending_videos` and `bronze_video_categories` datasets

### 2. Silver Layer (Data Cleaning & Standardization)
   - **Input**: Bronze layer datasets
   - **Process**:
     - Clean text fields (trim whitespace)
     - Convert data types (timestamps, numerics)
     - Handle missing values
     - Add derived metrics (engagement rate, like ratio)
     - Parse tags into lists
   - **Output**: `silver_trending_videos` and `silver_video_categories` datasets

### 3. Gold Layer (Analytics-Ready Data)
   - **Input**: Silver layer datasets
   - **Process**:
     - Create dimension tables:
       - `dim_videos`: Unique videos with attributes
       - `dim_channels`: Unique channels
       - `dim_categories`: Video categories
       - `dim_regions`: Geographic regions
     - Create fact table:
       - `fact_trending_videos`: Trending video metrics with foreign keys
     - Create aggregated tables:
       - `agg_region_trends`: Metrics by region
       - `agg_category_performance`: Metrics by category
   - **Output**: Star schema in PostgreSQL database

## Verification Process

1. **Data Quality Checks**
   - Verify row counts match between layers
   - Check for missing values in key fields
   - Validate foreign key relationships

2. **Access the Processed Data**
   - Connect to PostgreSQL: `psql -h localhost -p 5432 -U postgres -d youtube_analytics`
   - Query the gold layer tables:
     ```sql
     SELECT * FROM gold.dim_regions;
     SELECT * FROM gold.dim_categories;
     SELECT * FROM gold.fact_trending_videos LIMIT 10;
     SELECT * FROM gold.agg_region_trends LIMIT 10;
     ```

3. **Monitoring**
   - Check Dagster logs for any errors
   - Monitor resource usage in Docker containers
   - Verify data lineage through metadata

## Troubleshooting

1. **Database Connection Issues**
   - Verify Docker containers are running: `docker ps`
   - Check database logs: `docker logs youtube-etl-pipeline_mysql_1`
   - Ensure correct credentials are being used

2. **Data Loading Problems**
   - Verify CSV files exist and have the correct format
   - Check for encoding issues in CSV files
   - Look for error messages in the load script output

3. **Pipeline Execution Failures**
   - Check Dagster UI for detailed error messages
   - Verify resource availability (disk space, memory)
   - Ensure all dependencies are correctly installed
