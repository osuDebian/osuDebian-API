select
    R.beatmap_id,
    R.userid,
    R.top_rank,
    R.rank,
    R.play_mode,
    R.time,
    bmap.song_name
from  ( select * from 
    (SELECT id, RANK() OVER (PARTITION BY beatmap_id ORDER BY pp DESC) AS top_rank,
    beatmap_id,userid,pp,beatmap_md5, time, rank, play_mode
    FROM Ainu.scores where completed = 3 and play_mode = {1} and pp >= 1 order by time desc) as R
where userid = {0} limit {2}) as R  
left join
    (select song_name, beatmap_id from Ainu.beatmaps) as bmap on bmap.beatmap_id = R.beatmap_id
order by R.time desc
;