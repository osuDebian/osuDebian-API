SELECT  A.beatmap_id 
       ,beatmapset_id 
       ,userid 
       ,RANKING 
       ,pp 
       ,time    AS play_time 
       ,mods 
       ,id      AS score_id 
       ,play_mode 
       ,accuracy 
       ,rank 
       ,title   AS beatmap_title 
       ,artist  AS beatmap_artist 
       ,version AS beatmap_version
FROM 
(
	SELECT  beatmap_id 
	       ,beatmapset_id 
	       ,userid 
	       ,pp 
	       ,time 
	       ,mods 
	       ,id 
	       ,play_mode 
	       ,accuracy 
	       ,rank 
	       ,ROW_NUMBER() OVER( PARTITION BY beatmap_id ORDER BY score DESC ) AS RANKING
	FROM 
	(
		SELECT  *
		FROM Ainu.scores aaa
		JOIN 
		(
			SELECT  id AS uid
			FROM Ainu.users
			WHERE not privileges = 0  
		) AS userdata
		ON userdata.uid = aaa.userid
		WHERE completed = 3 
		AND beatmap_id > 0 
		AND beatmapset_id > 0 
		AND not pp = 0 
		AND play_mode = {2}  
	) A 
) A
JOIN 
(
	SELECT  beatmap_id 
	       ,title 
	       ,artist 
	       ,version
	FROM Ainu.beatmaps
	WHERE not ranked = 0  
) AS beatmaps
ON beatmaps.beatmap_id = A.beatmap_id
WHERE RANKING = 1 
AND userid = {0}
ORDER BY pp desc 
LIMIT {1};