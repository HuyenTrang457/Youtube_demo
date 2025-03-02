"""Tests for the gold layer assets."""
import pandas as pd
import pytest
from unittest.mock import MagicMock

from etl_pipeline.assets.gold_layer import (
    dim_categories, dim_videos, dim_channels, dim_regions,
    fact_trending_videos, agg_region_trends, agg_category_performance
)


def test_dim_categories():
    """Test the dim_categories asset."""
    # Create a mock context
    mock_context = MagicMock()
    
    # Create a mock input DataFrame
    mock_df = pd.DataFrame({
        "category_id": [1, 2, 10],
        "category_name": ["Film & Animation", "Autos & Vehicles", "Music"],
        "processed_at": pd.to_datetime(["2023-01-01"] * 3)
    })
    
    # Call the asset function
    result = dim_categories(mock_context, mock_df)
    
    # Assert that the result is a DataFrame
    assert isinstance(result.value, pd.DataFrame)
    
    # Assert that the DataFrame has the expected columns
    assert "category_id" in result.value.columns
    assert "category_name" in result.value.columns
    
    # Assert that the processed_at column is not included
    assert "processed_at" not in result.value.columns
    
    # Assert that the metadata is correct
    assert result.metadata["schema"] == "youtube_analytics"
    assert result.metadata["if_exists"] == "replace"
    assert result.metadata["row_count"] == 3


def test_dim_videos():
    """Test the dim_videos asset."""
    # Create a mock context
    mock_context = MagicMock()
    
    # Create a mock input DataFrame with multiple versions of the same video
    mock_df = pd.DataFrame({
        "id": ["video1", "video2", "video1"],
        "title": ["Title 1", "Title 2", "Title 1 Updated"],
        "channel_title": ["Channel 1", "Channel 2", "Channel 1"],
        "publish_time": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-01"]),
        "trending_date": pd.to_datetime(["2023-01-02", "2023-01-03", "2023-01-04"]),  # Latest date for video1
        "thumbnail_link": ["https://example.com/thumb1.jpg", "https://example.com/thumb2.jpg", "https://example.com/thumb1_updated.jpg"],
        "comments_disabled": [False, False, False],
        "ratings_disabled": [False, False, False],
        "description": ["Description 1", "Description 2", "Description 1 Updated"],
        "category_id": [24, 10, 24],
        "tags": ["tag1,tag2", "tag3,tag4", "tag1,tag2,tag5"],
        "region": ["US", "US", "US"],
        "processed_at": pd.to_datetime(["2023-01-01"] * 3)
    })
    
    # Call the asset function
    result = dim_videos(mock_context, mock_df)
    
    # Assert that the result is a DataFrame
    assert isinstance(result.value, pd.DataFrame)
    
    # Assert that the DataFrame has the expected columns
    assert "video_key" in result.value.columns
    assert "id" in result.value.columns
    assert "title" in result.value.columns
    
    # Assert that only unique videos are included
    assert len(result.value) == 2
    
    # Assert that the latest version of video1 is used
    video1_row = result.value[result.value["id"] == "video1"]
    assert video1_row["title"].iloc[0] == "Title 1 Updated"
    assert video1_row["thumbnail_link"].iloc[0] == "https://example.com/thumb1_updated.jpg"
    
    # Assert that the metadata is correct
    assert result.metadata["schema"] == "youtube_analytics"
    assert result.metadata["if_exists"] == "replace"
    assert result.metadata["row_count"] == 2


def test_fact_trending_videos():
    """Test the fact_trending_videos asset."""
    # Create a mock context
    mock_context = MagicMock()
    
    # Create mock input DataFrames
    mock_trending_df = pd.DataFrame({
        "id": ["video1", "video2", "video1"],
        "channel_title": ["Channel 1", "Channel 2", "Channel 1"],
        "region": ["US", "US", "UK"],
        "category_id": [24, 10, 24],
        "trending_date": pd.to_datetime(["2023-01-02", "2023-01-03", "2023-01-02"]),
        "view_count": [100000, 200000, 90000],
        "likes": [5000, 10000, 4500],
        "dislikes": [100, 200, 90],
        "comment_count": [300, 500, 270],
        "engagement_rate": [0.054, 0.0535, 0.054],
        "like_ratio": [0.98, 0.98, 0.98],
        "processed_at": pd.to_datetime(["2023-01-01"] * 3)
    })
    
    mock_dim_videos = pd.DataFrame({
        "video_key": [1, 2],
        "id": ["video1", "video2"],
        "title": ["Title 1", "Title 2"]
    })
    
    mock_dim_channels = pd.DataFrame({
        "channel_key": [1, 2],
        "channel_title": ["Channel 1", "Channel 2"]
    })
    
    mock_dim_regions = pd.DataFrame({
        "region_key": [1, 2],
        "region": ["US", "UK"],
        "region_name": ["United States", "United Kingdom"]
    })
    
    # Call the asset function
    result = fact_trending_videos(mock_context, mock_trending_df, mock_dim_videos, mock_dim_channels, mock_dim_regions)
    
    # Assert that the result is a DataFrame
    assert isinstance(result.value, pd.DataFrame)
    
    # Assert that the DataFrame has the expected columns
    assert "trending_key" in result.value.columns
    assert "video_key" in result.value.columns
    assert "channel_key" in result.value.columns
    assert "region_key" in result.value.columns
    
    # Assert that all rows are included
    assert len(result.value) == 3
    
    # Assert that the surrogate keys are correctly joined
    us_video1_row = result.value[(result.value["video_key"] == 1) & (result.value["region_key"] == 1)]
    assert len(us_video1_row) == 1
    assert us_video1_row["channel_key"].iloc[0] == 1
    
    # Assert that the metadata is correct
    assert result.metadata["schema"] == "youtube_analytics"
    assert result.metadata["if_exists"] == "replace"
    assert result.metadata["row_count"] == 3