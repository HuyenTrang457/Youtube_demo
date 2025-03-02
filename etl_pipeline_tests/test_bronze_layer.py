"""Tests for the bronze layer assets."""
import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from etl_pipeline.assets.bronze_layer import bronze_video_categories, bronze_trending_videos


def test_bronze_video_categories():
    """Test the bronze_video_categories asset."""
    # Create a mock context
    mock_context = MagicMock()
    
    # Create a mock MySQL IO manager
    mock_mysql_io_manager = MagicMock()
    mock_context.resources.mysql_io_manager = mock_mysql_io_manager
    
    # Create a mock DataFrame to return
    mock_df = pd.DataFrame({
        "category_id": [1, 2, 10],
        "category_name": ["Film & Animation", "Autos & Vehicles", "Music"]
    })
    
    # Configure the mock to return the DataFrame
    mock_mysql_io_manager.load_input.return_value = mock_df
    
    # Call the asset function
    result = bronze_video_categories(mock_context)
    
    # Assert that the result is a DataFrame
    assert isinstance(result.value, pd.DataFrame)
    
    # Assert that the DataFrame has the expected columns
    assert "category_id" in result.value.columns
    assert "category_name" in result.value.columns
    assert "extracted_at" in result.value.columns
    
    # Assert that the metadata is correct
    assert result.metadata["layer"] == "bronze"
    assert result.metadata["bucket"] == "bronze"
    assert result.metadata["format"] == "parquet"
    assert result.metadata["row_count"] == len(mock_df)
    assert result.metadata["num_categories"] == mock_df["category_id"].nunique()


def test_bronze_trending_videos():
    """Test the bronze_trending_videos asset."""
    # Create a mock context
    mock_context = MagicMock()
    
    # Create a mock MySQL IO manager
    mock_mysql_io_manager = MagicMock()
    mock_context.resources.mysql_io_manager = mock_mysql_io_manager
    
    # Create a mock DataFrame to return for each region
    mock_df_us = pd.DataFrame({
        "id": ["video1_us", "video2_us"],
        "title": ["US Video 1", "US Video 2"],
        "channel_title": ["US Channel 1", "US Channel 2"],
        "publish_time": ["2023-01-01", "2023-01-02"],
        "trending_date": ["2023-01-02", "2023-01-03"],
        "view_count": [100000, 200000],
        "likes": [5000, 10000],
        "dislikes": [100, 200],
        "comment_count": [300, 500],
        "thumbnail_link": ["https://example.com/thumb1.jpg", "https://example.com/thumb2.jpg"],
        "comments_disabled": [False, False],
        "ratings_disabled": [False, False],
        "description": ["Description 1", "Description 2"],
        "category_id": [24, 10],
        "tags": ["tag1,tag2", "tag3,tag4"],
        "region": ["US", "US"]
    })
    
    mock_df_uk = pd.DataFrame({
        "id": ["video1_uk", "video2_uk"],
        "title": ["UK Video 1", "UK Video 2"],
        "channel_title": ["UK Channel 1", "UK Channel 2"],
        "publish_time": ["2023-01-01", "2023-01-02"],
        "trending_date": ["2023-01-02", "2023-01-03"],
        "view_count": [90000, 180000],
        "likes": [4500, 9000],
        "dislikes": [90, 180],
        "comment_count": [270, 450],
        "thumbnail_link": ["https://example.com/thumb4.jpg", "https://example.com/thumb5.jpg"],
        "comments_disabled": [False, False],
        "ratings_disabled": [False, False],
        "description": ["UK Description 1", "UK Description 2"],
        "category_id": [24, 10],
        "tags": ["tag1,tag2", "tag3,tag4"],
        "region": ["UK", "UK"]
    })
    
    # Configure the mock to return different DataFrames for different regions
    def side_effect(context):
        asset_key = context.asset_key.path[0]
        if asset_key == "us_trending_videos":
            return mock_df_us
        elif asset_key == "uk_trending_videos":
            return mock_df_uk
        else:
            # Return empty DataFrame for other regions
            return pd.DataFrame()
    
    mock_mysql_io_manager.load_input.side_effect = side_effect
    
    # Patch the REGIONS list to only include US and UK for testing
    with patch("etl_pipeline.assets.bronze_layer.REGIONS", ["us", "uk"]):
        # Call the asset function
        result = bronze_trending_videos(mock_context)
    
    # Assert that the result is a DataFrame
    assert isinstance(result.value, pd.DataFrame)
    
    # Assert that the DataFrame has the expected number of rows
    assert len(result.value) == len(mock_df_us) + len(mock_df_uk)
    
    # Assert that the DataFrame has the expected columns
    assert "id" in result.value.columns
    assert "title" in result.value.columns
    assert "region" in result.value.columns
    assert "extracted_at" in result.value.columns
    
    # Assert that the metadata is correct
    assert result.metadata["layer"] == "bronze"
    assert result.metadata["bucket"] == "bronze"
    assert result.metadata["format"] == "parquet"
    assert result.metadata["row_count"] == len(result.value)
    assert result.metadata["num_regions"] == 2  # US and UK
    assert result.metadata["num_videos"] == 4  # 2 from US, 2 from UK