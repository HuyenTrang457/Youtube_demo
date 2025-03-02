-- Insert sample data for US region
INSERT INTO us_trending_videos 
(id, title, channel_title, publish_time, trending_date, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled, description, category_id, tags)
VALUES
('video1_us', 'Sample US Video 1', 'US Channel 1', '2023-01-01 12:00:00', '2023-01-02', 100000, 5000, 100, 300, 'https://example.com/thumb1.jpg', false, false, 'This is a sample video description', 24, 'entertainment,sample,trending'),
('video2_us', 'Sample US Video 2', 'US Channel 2', '2023-01-02 14:30:00', '2023-01-03', 200000, 10000, 200, 500, 'https://example.com/thumb2.jpg', false, false, 'Another sample video description', 10, 'music,trending,popular'),
('video3_us', 'Sample US Video 3', 'US Channel 3', '2023-01-03 09:15:00', '2023-01-04', 150000, 7500, 150, 400, 'https://example.com/thumb3.jpg', false, false, 'Yet another sample video description', 20, 'gaming,sample,trending');

-- Insert sample data for UK region
INSERT INTO uk_trending_videos 
(id, title, channel_title, publish_time, trending_date, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled, description, category_id, tags)
VALUES
('video1_uk', 'Sample UK Video 1', 'UK Channel 1', '2023-01-01 10:00:00', '2023-01-02', 90000, 4500, 90, 270, 'https://example.com/thumb4.jpg', false, false, 'UK sample video description', 24, 'entertainment,sample,trending,uk'),
('video2_uk', 'Sample UK Video 2', 'UK Channel 2', '2023-01-02 13:30:00', '2023-01-03', 180000, 9000, 180, 450, 'https://example.com/thumb5.jpg', false, false, 'Another UK sample video description', 10, 'music,trending,popular,uk'),
('video3_uk', 'Sample UK Video 3', 'UK Channel 3', '2023-01-03 08:15:00', '2023-01-04', 135000, 6750, 135, 360, 'https://example.com/thumb6.jpg', false, false, 'Yet another UK sample video description', 20, 'gaming,sample,trending,uk');

-- Insert sample data for Canada region
INSERT INTO ca_trending_videos 
(id, title, channel_title, publish_time, trending_date, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled, description, category_id, tags)
VALUES
('video1_ca', 'Sample CA Video 1', 'CA Channel 1', '2023-01-01 11:00:00', '2023-01-02', 85000, 4250, 85, 255, 'https://example.com/thumb7.jpg', false, false, 'CA sample video description', 24, 'entertainment,sample,trending,ca'),
('video2_ca', 'Sample CA Video 2', 'CA Channel 2', '2023-01-02 12:30:00', '2023-01-03', 170000, 8500, 170, 425, 'https://example.com/thumb8.jpg', false, false, 'Another CA sample video description', 10, 'music,trending,popular,ca'),
('video3_ca', 'Sample CA Video 3', 'CA Channel 3', '2023-01-03 07:15:00', '2023-01-04', 127500, 6375, 127, 340, 'https://example.com/thumb9.jpg', false, false, 'Yet another CA sample video description', 20, 'gaming,sample,trending,ca');