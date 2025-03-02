{{
    config(
        materialized='table',
        schema='silver'
    )
}}

WITH source_data AS (
    SELECT 
        id,
        title,
        channel_title,
        publish_time,
        trending_date,
        view_count,
        likes,
        dislikes,
        comment_count,
        thumbnail_link,
        comments_disabled,
        ratings_disabled,
        description,
        category_id,
        tags,
        region,
        extracted_at
    FROM {{ source('bronze', 'trending_videos') }}
)

SELECT
    id,
    TRIM(title) AS title,
    TRIM(channel_title) AS channel_title,
    CAST(publish_time AS TIMESTAMP) AS publish_time,
    CAST(trending_date AS DATE) AS trending_date,
    COALESCE(view_count, 0) AS view_count,
    COALESCE(likes, 0) AS likes,
    COALESCE(dislikes, 0) AS dislikes,
    COALESCE(comment_count, 0) AS comment_count,
    thumbnail_link,
    COALESCE(comments_disabled, FALSE) AS comments_disabled,
    COALESCE(ratings_disabled, FALSE) AS ratings_disabled,
    description,
    category_id,
    tags,
    region,
    extracted_at,
    CURRENT_TIMESTAMP AS processed_at,
    
    -- Derived metrics
    CASE 
        WHEN COALESCE(view_count, 0) = 0 THEN 0
        ELSE (COALESCE(likes, 0) + COALESCE(dislikes, 0) + COALESCE(comment_count, 0)) / NULLIF(view_count, 0)
    END AS engagement_rate,
    
    CASE 
        WHEN (COALESCE(likes, 0) + COALESCE(dislikes, 0)) = 0 THEN 0
        ELSE COALESCE(likes, 0) / NULLIF((COALESCE(likes, 0) + COALESCE(dislikes, 0)), 0)
    END AS like_ratio
FROM source_data