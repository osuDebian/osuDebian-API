SELECT SQL_CACHE json_object(
	'rankedby',			rankedby, 
	'beatmap_id',		beatmap_id, 
	'beatmapset_id',	beatmapset_id,
	'beatmap_md5',		debian.beatmap_md5, 
	'ranking_time',		FROM_UNIXTIME(debian.latest_update, '%Y-%m-%d %H:%i'), 
	'ranked',			(CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END), 
	'song_name',		debian.song_name, 
	'title',			title, 
	'artist',			artist, 
	'creator',			creator, 
	'time',				debian.hit_length, 
	'mode',				debian.mode, 
	'diff',				CAST(debian.difficulty_{1} AS float), 
	'bpm',				debian.bpm, 
	'ar',				debian.ar, 
	'cs',				debian.cs, 
	'od',				debian.od, 
	'hp',				debian.hp, 
	'playcount',		debian.playcount, 
	'passcount',		debian.passcount, 
	'max_combo',		debian.max_combo 
) as data
FROM Ainu.beatmaps as debian WHERE beatmap_id = {0};