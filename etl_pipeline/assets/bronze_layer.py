"""Bronze layer assets for the ETL pipeline."""
import pandas as pd
from dagster import asset, AssetIn, Output, MetadataValue

# Define the regions
REGIONS = ["us", "uk", "ca", "de", "fr", "jp", "au", "in", "br", "kr"]


@asset(
    group_name="bronze",
    metadata={
        "layer": "bronze",
        "description": "Raw trending videos data from MySQL",
    },
    io_manager_key="minio_io_manager",
)
def bronze_video_categories(context) -> Output[pd.DataFrame]:
    """Extract video categories from MySQL and store in MinIO bronze layer."""
    # Use the MySQL IO manager to load data
    mysql_io_manager = context.resources.mysql_io_manager
    
    # Load categories data
    query = "SELECT * FROM video_categories"
    df = mysql_io_manager.load_input(
        context.build_input_context(
            asset_key=["video_categories"],
            metadata={"query": query},
        )
    )
    
    # Add extraction timestamp
    df["extracted_at"] = pd.Timestamp.now()
    
    # Return the data with metadata for MinIO storage
    return Output(
        df,
        metadata={
            "layer": "bronze",
            "bucket": "bronze",
            "format": "parquet",
            "row_count": len(df),
            "num_categories": df["category_id"].nunique(),
        },
    )


@asset(
    group_name="bronze",
    metadata={
        "layer": "bronze",
        "description": "Raw trending videos data from MySQL by region",
    },
    io_manager_key="minio_io_manager",
)
def bronze_trending_videos(context) -> Output[pd.DataFrame]:
    """Extract trending videos from all regions in MySQL and store in MinIO bronze layer."""
    # Use the MySQL IO manager to load data
    mysql_io_manager = context.resources.mysql_io_manager
    
    # Initialize an empty list to store DataFrames from each region
    all_regions_data = []
    
    # Load data from each region
    for region in REGIONS:
        table_name = f"{region}_trending_videos"
        query = f"SELECT * FROM {table_name}"
        
        try:
            df = mysql_io_manager.load_input(
                context.build_input_context(
                    asset_key=[table_name],
                    metadata={"query": query},
                )
            )
            
            # Add extraction timestamp
            df["extracted_at"] = pd.Timestamp.now()
            
            # Add to the list
            all_regions_data.append(df)
            context.log.info(f"Loaded {len(df)} rows from {table_name}")
        except Exception as e:
            context.log.error(f"Error loading data from {table_name}: {str(e)}")
    
    # Combine all regions' data
    if not all_regions_data:
        context.log.error("No data loaded from any region")
        return Output(
            pd.DataFrame(),
            metadata={
                "layer": "bronze",
                "bucket": "bronze",
                "format": "parquet",
                "row_count": 0,
                "error": "No data loaded",
            },
        )
    
    combined_df = pd.concat(all_regions_data, ignore_index=True)
    
    # Return the data with metadata for MinIO storage
    return Output(
        combined_df,
        metadata={
            "layer": "bronze",
            "bucket": "bronze",
            "format": "parquet",
            "partitioning": ["region", "trending_date"],
            "row_count": len(combined_df),
            "num_regions": combined_df["region"].nunique(),
            "num_videos": combined_df["id"].nunique(),
            "date_range": f"{combined_df['trending_date'].min()} to {combined_df['trending_date'].max()}",
        },
    )