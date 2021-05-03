SELECT
    rr.playcount,
	rr.beatmap_id,
    bmap.beatmapset_id,
    bmap.song_name,
    bmap.creator
FROM
	(select beatmap_id, playcount from Ainu.rx_beatmap_playcount WHERE user_id = {0} order by playcount desc limit {1}) as rr
left join
	(select beatmap_id, beatmapset_id, song_name, creator from Ainu.beatmaps) as bmap on bmap.beatmap_id = rr.beatmap_id
order by rr.playcount desc;