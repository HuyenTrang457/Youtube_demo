"""Tests for the silver layer assets."""
import pandas as pd
import pytest
from unittest.mock import MagicMock

from etl_pipeline.assets.silver_layer import silver_video_categories, silver_trending_videos


def test_silver_video_categories():
    """Test the silver_video_categories asset."""
    # Create a mock context
    mock_context = MagicMock()
    
    # Create a mock input DataFrame
    mock_df = pd.DataFrame({
        "category_id": [1, 2, 10, 2],  # Duplicate category_id
        "category_name": [" Film & Animation ", "autos & vehicles", "Music ", "Autos & Vehicles"],
        "extracted_at": pd.to_datetime(["2023-01-01"] * 4)
    })
    
    # Call the asset function
    result = silver_video_categories(mock_context, mock_df)
    
    # Assert that the result is a DataFrame
    assert isinstance(result.value, pd.DataFrame)
    
    # Assert that duplicates are removed
    assert len(result.value) == 3
    
    # Assert that category names are cleaned
    assert result.value["category_name"].iloc[0] == "Film & Animation"
    assert result.value["category_name"].iloc[1] == "Autos & Vehicles"
    
    # Assert that the processed_at column is added
    assert "processed_at" in result.value.columns
    
    # Assert that the metadata is correct
    assert result.metadata["layer"] == "silver"
    assert result.metadata["bucket"] == "silver"
    assert result.metadata["format"] == "parquet"
    assert result.metadata["row_count"] == 3
    assert result.metadata["num_categories"] == 3


def test_silver_trending_videos():
    """Test the silver_trending_videos asset."""
    # Create a mock context
    mock_context = MagicMock()
    
    # Create a mock input DataFrame with various issues to clean
    mock_df = pd.DataFrame({
        "id": ["video1", "video2", "video1"],  # Duplicate id
        "title": [" Title 1 ", "Title 2", "Title 1"],
        "channel_title": ["Channel 1 ", " Channel 2", "Channel 1"],
        "publish_time": ["2023-01-01 12:00:00", "2023-01-02 14:30:00", "2023-01-01 12:00:00"],
        "trending_date": ["2023-01-02", "2023-01-03", "2023-01-02"],
        "view_count": [100000, None, 100000],  # None value
        "likes": [5000, 10000, 5000],
        "dislikes": [100, None, 100],  # None value
        "comment_count": [300, 500, 300],
        "thumbnail_link": ["https://example.com/thumb1.jpg", "https://example.com/thumb2.jpg", "https://example.com/thumb1.jpg"],
        "comments_disabled": [False, None, False],  # None value
        "ratings_disabled": [False, False, False],
        "description": ["Description 1", "Description 2", "Description 1"],
        "category_id": [24, 10, 24],
        "tags": ["tag1,tag2", "tag3,tag4", "tag1,tag2"],
        "region": ["US", "US", "US"],
        "extracted_at": pd.to_datetime(["2023-01-01"] * 3)
    })
    
    # Call the asset function
    result = silver_trending_videos(mock_context, mock_df)
    
    # Assert that the result is a DataFrame
    assert isinstance(result.value, pd.DataFrame)
    
    # Assert that duplicates are removed
    assert len(result.value) == 2
    
    # Assert that missing values are filled
    assert result.value["view_count"].isna().sum() == 0
    assert result.value["likes"].isna().sum() == 0
    assert result.value["dislikes"].isna().sum() == 0
    assert result.value["comment_count"].isna().sum() == 0
    
    # Assert that text fields are cleaned
    assert result.value["title"].iloc[0] == "Title 1"
    assert result.value["channel_title"].iloc[0] == "Channel 1"
    
    # Assert that timestamps are standardized
    assert isinstance(result.value["publish_time"].iloc[0], pd.Timestamp)
    assert isinstance(result.value["trending_date"].iloc[0], pd.Timestamp)
    
    # Assert that derived metrics are added
    assert "engagement_rate" in result.value.columns
    assert "like_ratio" in result.value.columns
    
    # Assert that tags are parsed into a list
    assert "tags_list" in result.value.columns
    assert isinstance(result.value["tags_list"].iloc[0], list)
    
    # Assert that the processed_at column is added
    assert "processed_at" in result.value.columns
    
    # Assert that the metadata is correct
    assert result.metadata["layer"] == "silver"
    assert result.metadata["bucket"] == "silver"
    assert result.metadata["format"] == "parquet"
    assert result.metadata["row_count"] == 2
    assert result.metadata["num_regions"] == 1
    assert result.metadata["num_videos"] == 2