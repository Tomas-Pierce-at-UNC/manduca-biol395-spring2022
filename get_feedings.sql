SELECT * 
FROM videos 
INNER JOIN feedings
ON videos.video_id = feedings.video_id;