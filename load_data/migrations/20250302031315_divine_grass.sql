{{
    config(
        materialized='table',
        schema='gold'
    )
}}

WITH trending_data AS (
    SELECT
        v.id,
        v.channel_title,
        v.region,
        v.category_id,
        v.trending_date,
        v.view_count,
        v.likes,
        v.dislikes,
        v.comment_count,
        v.engagement_rate,
        v.like_ratio
    FROM {{ ref('silver_trending_videos') }} v
)

SELECT
    ROW_NUMBER() OVER (ORDER BY t.trending_date, t.id) AS trending_key,
    dv.video_key,
    dc.channel_key,
    dr.region_key,
    t.category_id,
    t.trending_date,
    t.view_count,
    t.likes,
    t.dislikes,
    t.comment_count,
    t.engagement_rate,
    t.like_ratio
FROM trending_data t
JOIN {{ ref('dim_videos') }} dv ON t.id = dv.id
JOIN {{ ref('dim_channels') }} dc ON t.channel_title = dc.channel_title
JOIN {{ ref('dim_regions') }} dr ON t.region = dr.region