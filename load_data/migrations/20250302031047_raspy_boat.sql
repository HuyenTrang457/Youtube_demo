-- Create database schema for YouTube data
USE youtube_data;

-- Create tables for 10 regions
-- We'll create one table per region to simulate multiple data sources

-- US Region
CREATE TABLE IF NOT EXISTS us_trending_videos (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    channel_title VARCHAR(255),
    publish_time DATETIME,
    trending_date DATE,
    view_count BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link VARCHAR(255),
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    description TEXT,
    category_id INT,
    tags TEXT,
    region VARCHAR(10) DEFAULT 'US'
);

-- UK Region
CREATE TABLE IF NOT EXISTS uk_trending_videos (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    channel_title VARCHAR(255),
    publish_time DATETIME,
    trending_date DATE,
    view_count BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link VARCHAR(255),
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    description TEXT,
    category_id INT,
    tags TEXT,
    region VARCHAR(10) DEFAULT 'UK'
);

-- Canada Region
CREATE TABLE IF NOT EXISTS ca_trending_videos (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    channel_title VARCHAR(255),
    publish_time DATETIME,
    trending_date DATE,
    view_count BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link VARCHAR(255),
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    description TEXT,
    category_id INT,
    tags TEXT,
    region VARCHAR(10) DEFAULT 'CA'
);

-- Germany Region
CREATE TABLE IF NOT EXISTS de_trending_videos (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    channel_title VARCHAR(255),
    publish_time DATETIME,
    trending_date DATE,
    view_count BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link VARCHAR(255),
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    description TEXT,
    category_id INT,
    tags TEXT,
    region VARCHAR(10) DEFAULT 'DE'
);

-- France Region
CREATE TABLE IF NOT EXISTS fr_trending_videos (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    channel_title VARCHAR(255),
    publish_time DATETIME,
    trending_date DATE,
    view_count BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link VARCHAR(255),
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    description TEXT,
    category_id INT,
    tags TEXT,
    region VARCHAR(10) DEFAULT 'FR'
);

-- Japan Region
CREATE TABLE IF NOT EXISTS jp_trending_videos (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    channel_title VARCHAR(255),
    publish_time DATETIME,
    trending_date DATE,
    view_count BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link VARCHAR(255),
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    description TEXT,
    category_id INT,
    tags TEXT,
    region VARCHAR(10) DEFAULT 'JP'
);

-- Australia Region
CREATE TABLE IF NOT EXISTS au_trending_videos (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    channel_title VARCHAR(255),
    publish_time DATETIME,
    trending_date DATE,
    view_count BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link VARCHAR(255),
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    description TEXT,
    category_id INT,
    tags TEXT,
    region VARCHAR(10) DEFAULT 'AU'
);

-- India Region
CREATE TABLE IF NOT EXISTS in_trending_videos (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    channel_title VARCHAR(255),
    publish_time DATETIME,
    trending_date DATE,
    view_count BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link VARCHAR(255),
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    description TEXT,
    category_id INT,
    tags TEXT,
    region VARCHAR(10) DEFAULT 'IN'
);

-- Brazil Region
CREATE TABLE IF NOT EXISTS br_trending_videos (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    channel_title VARCHAR(255),
    publish_time DATETIME,
    trending_date DATE,
    view_count BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link VARCHAR(255),
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    description TEXT,
    category_id INT,
    tags TEXT,
    region VARCHAR(10) DEFAULT 'BR'
);

-- South Korea Region
CREATE TABLE IF NOT EXISTS kr_trending_videos (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    channel_title VARCHAR(255),
    publish_time DATETIME,
    trending_date DATE,
    view_count BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    thumbnail_link VARCHAR(255),
    comments_disabled BOOLEAN,
    ratings_disabled BOOLEAN,
    description TEXT,
    category_id INT,
    tags TEXT,
    region VARCHAR(10) DEFAULT 'KR'
);

-- Categories table (shared across regions)
CREATE TABLE IF NOT EXISTS video_categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- Insert some sample category data
INSERT INTO video_categories (category_id, category_name) VALUES
(1, 'Film & Animation'),
(2, 'Autos & Vehicles'),
(10, 'Music'),
(15, 'Pets & Animals'),
(17, 'Sports'),
(18, 'Short Movies'),
(19, 'Travel & Events'),
(20, 'Gaming'),
(21, 'Videoblogging'),
(22, 'People & Blogs'),
(23, 'Comedy'),
(24, 'Entertainment'),
(25, 'News & Politics'),
(26, 'Howto & Style'),
(27, 'Education'),
(28, 'Science & Technology'),
(29, 'Nonprofits & Activism'),
(30, 'Movies'),
(31, 'Anime/Animation'),
(32, 'Action/Adventure'),
(33, 'Classics'),
(34, 'Comedy'),
(35, 'Documentary'),
(36, 'Drama'),
(37, 'Family'),
(38, 'Foreign'),
(39, 'Horror'),
(40, 'Sci-Fi/Fantasy'),
(41, 'Thriller'),
(42, 'Shorts'),
(43, 'Shows'),
(44, 'Trailers');