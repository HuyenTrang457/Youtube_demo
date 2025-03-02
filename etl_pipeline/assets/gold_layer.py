"""Gold layer assets for the ETL pipeline."""
import pandas as pd
from dagster import asset, AssetIn, Output, MetadataValue


@asset(
    group_name="gold",
    ins={
        "silver_video_categories": AssetIn(key="silver_video_categories"),
    },
    metadata={
        "layer": "gold",
        "description": "Dimension table for video categories",
    },
    io_manager_key="postgres_io_manager",
)
def dim_categories(context, silver_video_categories: pd.DataFrame) -> Output[pd.DataFrame]:
    """Create dimension table for video categories."""
    # Make a copy to avoid modifying the input
    df = silver_video_categories.copy()
    
    # Select only the columns needed for the dimension table
    dim_df = df[["category_id", "category_name"]].copy()
    
    # Return the dimension table
    return Output(
        dim_df,
        metadata={
            "schema": "youtube_analytics",
            "if_exists": "replace",
            "row_count": len(dim_df),
        },
    )


@asset(
    group_name="gold",
    ins={
        "silver_trending_videos": AssetIn(key="silver_trending_videos"),
    },
    metadata={
        "layer": "gold",
        "description": "Dimension table for videos",
    },
    io_manager_key="postgres_io_manager",
)
def dim_videos(context, silver_trending_videos: pd.DataFrame) -> Output[pd.DataFrame]:
    """Create dimension table for videos."""
    # Make a copy to avoid modifying the input
    df = silver_trending_videos.copy()
    
    # Select only unique videos with their attributes
    video_cols = [
        "id", "title", "channel_title", "publish_time", 
        "thumbnail_link", "comments_disabled", "ratings_disabled", 
        "description", "category_id", "tags"
    ]
    
    # Get the latest version of each video
    dim_df = df.sort_values("trending_date", ascending=False).drop_duplicates(subset=["id"])
    dim_df = dim_df[video_cols].copy()
    
    # Add a surrogate key
    dim_df["video_key"] = range(1, len(dim_df) + 1)
    
    # Return the dimension table
    return Output(
        dim_df,
        metadata={
            "schema": "youtube_analytics",
            "if_exists": "replace",
            "row_count": len(dim_df),
        },
    )


@asset(
    group_name="gold",
    ins={
        "silver_trending_videos": AssetIn(key="silver_trending_videos"),
    },
    metadata={
        "layer": "gold",
        "description": "Dimension table for channels",
    },
    io_manager_key="postgres_io_manager",
)
def dim_channels(context, silver_trending_videos: pd.DataFrame) -> Output[pd.DataFrame]:
    """Create dimension table for channels."""
    # Make a copy to avoid modifying the input
    df = silver_trending_videos.copy()
    
    # Extract unique channels
    channels_df = df[["channel_title"]].drop_duplicates()
    
    # Add a surrogate key
    channels_df["channel_key"] = range(1, len(channels_df) + 1)
    
    # Return the dimension table
    return Output(
        channels_df,
        metadata={
            "schema": "youtube_analytics",
            "if_exists": "replace",
            "row_count": len(channels_df),
        },
    )


@asset(
    group_name="gold",
    ins={
        "silver_trending_videos": AssetIn(key="silver_trending_videos"),
    },
    metadata={
        "layer": "gold",
        "description": "Dimension table for regions",
    },
    io_manager_key="postgres_io_manager",
)
def dim_regions(context, silver_trending_videos: pd.DataFrame) -> Output[pd.DataFrame]:
    """Create dimension table for regions."""
    # Make a copy to avoid modifying the input
    df = silver_trending_videos.copy()
    
    # Extract unique regions
    regions_df = df[["region"]].drop_duplicates()
    
    # Add region names
    region_names = {
        "US": "United States",
        "UK": "United Kingdom",
        "CA": "Canada",
        "DE": "Germany",
        "FR": "France",
        "JP": "Japan",
        "AU": "Australia",
        "IN": "India",
        "BR": "Brazil",
        "KR": "South Korea",
    }
    
    regions_df["region_name"] = regions_df["region"].map(region_names)
    
    # Add a surrogate key
    regions_df["region_key"] = range(1, len(regions_df) + 1)
    
    # Return the dimension table
    return Output(
        regions_df,
        metadata={
            "schema": "youtube_analytics",
            "if_exists": "replace",
            "row_count": len(regions_df),
        },
    )


@asset(
    group_name="gold",
    ins={
        "silver_trending_videos": AssetIn(key="silver_trending_videos"),
        "dim_videos": AssetIn(key="dim_videos"),
        "dim_channels": AssetIn(key="dim_channels"),
        "dim_regions": AssetIn(key="dim_regions"),
    },
    metadata={
        "layer": "gold",
        "description": "Fact table for trending videos",
    },
    io_manager_key="postgres_io_manager",
)
def fact_trending_videos(
    context, 
    silver_trending_videos: pd.DataFrame,
    dim_videos: pd.DataFrame,
    dim_channels: pd.DataFrame,
    dim_regions: pd.DataFrame,
) -> Output[pd.DataFrame]:
    """Create fact table for trending videos."""
    # Make a copy to avoid modifying the input
    df = silver_trending_videos.copy()
    
    # Join with dimension tables to get surrogate keys
    df = df.merge(dim_videos[["id", "video_key"]], on="id", how="left")
    df = df.merge(dim_channels[["channel_title", "channel_key"]], on="channel_title", how="left")
    df = df.merge(dim_regions[["region", "region_key"]], on="region", how="left")
    
    # Select columns for the fact table
    fact_cols = [
        "video_key", "channel_key", "region_key", "category_id",
        "trending_date", "view_count", "likes", "dislikes", 
        "comment_count", "engagement_rate", "like_ratio"
    ]
    
    fact_df = df[fact_cols].copy()
    
    # Add a surrogate key for the fact table
    fact_df["trending_key"] = range(1, len(fact_df) + 1)
    
    # Return the fact table
    return Output(
        fact_df,
        metadata={
            "schema": "youtube_analytics",
            "if_exists": "replace",
            "row_count": len(fact_df),
        },
    )


@asset(
    group_name="gold",
    ins={
        "fact_trending_videos": AssetIn(key="fact_trending_videos"),
        "dim_regions": AssetIn(key="dim_regions"),
        "dim_categories": AssetIn(key="dim_categories"),
    },
    metadata={
        "layer": "gold",
        "description": "Aggregated metrics by region",
    },
    io_manager_key="postgres_io_manager",
)
def agg_region_trends(
    context, 
    fact_trending_videos: pd.DataFrame,
    dim_regions: pd.DataFrame,
    dim_categories: pd.DataFrame,
) -> Output[pd.DataFrame]:
    """Create aggregated metrics by region."""
    # Join with dimension tables
    df = fact_trending_videos.merge(dim_regions, on="region_key", how="left")
    df = df.merge(dim_categories, on="category_id", how="left")
    
    # Group by region and calculate aggregates
    agg_df = df.groupby(["region_key", "region", "region_name"]).agg(
        total_videos=("video_key", "nunique"),
        total_views=("view_count", "sum"),
        total_likes=("likes", "sum"),
        total_dislikes=("dislikes", "sum"),
        total_comments=("comment_count", "sum"),
        avg_engagement=("engagement_rate", "mean"),
        avg_like_ratio=("like_ratio", "mean"),
    ).reset_index()
    
    # Add timestamp
    agg_df["updated_at"] = pd.Timestamp.now()
    
    # Return the aggregated table
    return Output(
        agg_df,
        metadata={
            "schema": "youtube_analytics",
            "if_exists": "replace",
            "row_count": len(agg_df),
        },
    )


@asset(
    group_name="gold",
    ins={
        "fact_trending_videos": AssetIn(key="fact_trending_videos"),
        "dim_categories": AssetIn(key="dim_categories"),
    },
    metadata={
        "layer": "gold",
        "description": "Aggregated metrics by category",
    },
    io_manager_key="postgres_io_manager",
)
def agg_category_performance(
    context, 
    fact_trending_videos: pd.DataFrame,
    dim_categories: pd.DataFrame,
) -> Output[pd.DataFrame]:
    """Create aggregated metrics by category."""
    # Join with dimension tables
    df = fact_trending_videos.merge(dim_categories, on="category_id", how="left")
    
    # Group by category and calculate aggregates
    agg_df = df.groupby(["category_id", "category_name"]).agg(
        total_videos=("video_key", "nunique"),
        total_views=("view_count", "sum"),
        total_likes=("likes", "sum"),
        total_dislikes=("dislikes", "sum"),
        total_comments=("comment_count", "sum"),
        avg_engagement=("engagement_rate", "mean"),
        avg_like_ratio=("like_ratio", "mean"),
    ).reset_index()
    
    # Add timestamp
    agg_df["updated_at"] = pd.Timestamp.now()
    
    # Return the aggregated table
    return Output(
        agg_df,
        metadata={
            "schema": "youtube_analytics",
            "if_exists": "replace",
            "row_count": len(agg_df),
        },
    )