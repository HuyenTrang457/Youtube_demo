"""Silver layer assets for the ETL pipeline."""
import pandas as pd
from dagster import asset, AssetIn, Output, MetadataValue


@asset(
    group_name="silver",
    ins={
        "bronze_video_categories": AssetIn(key="bronze_video_categories"),
    },
    metadata={
        "layer": "silver",
        "description": "Cleaned and standardized video categories",
    },
    io_manager_key="minio_io_manager",
)
def silver_video_categories(context, bronze_video_categories: pd.DataFrame) -> Output[pd.DataFrame]:
    """Clean and standardize video categories data."""
    # Make a copy to avoid modifying the input
    df = bronze_video_categories.copy()
    
    # Clean category names (trim whitespace, standardize case)
    df["category_name"] = df["category_name"].str.strip().str.title()
    
    # Remove duplicates if any
    df = df.drop_duplicates(subset=["category_id"])
    
    # Add processing timestamp
    df["processed_at"] = pd.Timestamp.now()
    
    # Return the cleaned data
    return Output(
        df,
        metadata={
            "layer": "silver",
            "bucket": "silver",
            "format": "parquet",
            "row_count": len(df),
            "num_categories": df["category_id"].nunique(),
        },
    )


@asset(
    group_name="silver",
    ins={
        "bronze_trending_videos": AssetIn(key="bronze_trending_videos"),
    },
    metadata={
        "layer": "silver",
        "description": "Cleaned and standardized trending videos data",
    },
    io_manager_key="minio_io_manager",
)
def silver_trending_videos(context, bronze_trending_videos: pd.DataFrame) -> Output[pd.DataFrame]:
    """Clean and standardize trending videos data."""
    # Make a copy to avoid modifying the input
    df = bronze_trending_videos.copy()
    
    # Handle missing values
    df["view_count"] = df["view_count"].fillna(0)
    df["likes"] = df["likes"].fillna(0)
    df["dislikes"] = df["dislikes"].fillna(0)
    df["comment_count"] = df["comment_count"].fillna(0)
    
    # Convert to appropriate data types
    df["view_count"] = df["view_count"].astype(int)
    df["likes"] = df["likes"].astype(int)
    df["dislikes"] = df["dislikes"].astype(int)
    df["comment_count"] = df["comment_count"].astype(int)
    
    # Standardize timestamps
    df["publish_time"] = pd.to_datetime(df["publish_time"])
    df["trending_date"] = pd.to_datetime(df["trending_date"])
    
    # Clean text fields
    df["title"] = df["title"].str.strip()
    df["channel_title"] = df["channel_title"].str.strip()
    
    # Parse tags into a list
    df["tags_list"] = df["tags"].str.split(",")
    
    # Add derived metrics
    df["engagement_rate"] = (df["likes"] + df["dislikes"] + df["comment_count"]) / df["view_count"].replace(0, 1)
    df["like_ratio"] = df["likes"] / (df["likes"] + df["dislikes"]).replace(0, 1)
    
    # Add processing timestamp
    df["processed_at"] = pd.Timestamp.now()
    
    # Remove duplicates
    df = df.drop_duplicates(subset=["id", "trending_date", "region"])
    
    # Return the cleaned data
    return Output(
        df,
        metadata={
            "layer": "silver",
            "bucket": "silver",
            "format": "parquet",
            "partitioning": ["region", "trending_date"],
            "row_count": len(df),
            "num_regions": df["region"].nunique(),
            "num_videos": df["id"].nunique(),
            "date_range": f"{df['trending_date'].min()} to {df['trending_date'].max()}",
        },
    )