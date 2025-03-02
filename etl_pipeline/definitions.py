"""Definitions for the ETL pipeline."""
# Central file, defining all assets, jobs, schedules.
import os
from pathlib import Path

from dagster import Definitions, load_assets_from_modules, define_asset_job, ScheduleDefinition

from etl_pipeline.assets import bronze_layer, silver_layer, gold_layer
from etl_pipeline.resources.mysql_io_manager import MySQLIOManager
from etl_pipeline.resources.minio_io_manager import MinIOIOManager
from etl_pipeline.resources.psql_io_manager import PostgreSQLIOManager

# Load assets from modules
all_assets = load_assets_from_modules([bronze_layer, silver_layer, gold_layer])

# Define jobs
bronze_job = define_asset_job(
    name="bronze_extract_job",
    selection=["bronze_video_categories", "bronze_trending_videos"],
)

silver_job = define_asset_job(
    name="silver_transform_job",
    selection=["silver_video_categories", "silver_trending_videos"],
)

gold_job = define_asset_job(
    name="gold_load_job",
    selection=[
        "dim_categories", "dim_videos", "dim_channels", "dim_regions",
        "fact_trending_videos", "agg_region_trends", "agg_category_performance",
    ],
)

# Define schedules
bronze_schedule = ScheduleDefinition(
    job=bronze_job,
    cron_schedule="0 */6 * * *",  # Every 6 hours
)

silver_schedule = ScheduleDefinition(
    job=silver_job,
    cron_schedule="30 */6 * * *",  # Every 6 hours, 30 minutes after bronze
)

gold_schedule = ScheduleDefinition(
    job=gold_job,
    cron_schedule="0 */12 * * *",  # Every 12 hours
)

# Define resources
resources = {
    "mysql_io_manager": MySQLIOManager(),
    "minio_io_manager": MinIOIOManager(),
    "postgres_io_manager": PostgreSQLIOManager(),
}

# Define the Dagster definitions
defs = Definitions(
    assets=all_assets,
    jobs=[bronze_job, silver_job, gold_job],
    schedules=[bronze_schedule, silver_schedule, gold_schedule],
    resources=resources,
)