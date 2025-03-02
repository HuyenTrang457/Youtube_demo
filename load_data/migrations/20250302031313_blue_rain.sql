{{
    config(
        materialized='table',
        schema='gold'
    )
}}

WITH latest_videos AS (
    SELECT
        id,
        title,
        channel_title,
        publish_time,
        thumbnail_link,
        comments_disabled,
        ratings_disabled,
        description,
        category_id,
        tags,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY trending_date DESC) AS rn
    FROM {{ ref('silver_trending_videos') }}
)

SELECT
    ROW_NUMBER() OVER (ORDER BY id) AS video_key,
    id,
    title,
    channel_title,
    publish_time,
    thumbnail_link,
    comments_disabled,
    ratings_disabled,
    description,
    category_id,
    tags
FROM latest_videos
WHERE rn = 1