select
    scores.id as score_id,
    scores.userid as user_id,
    scores.time as play_time,
    scores.mods as mods,
    scores.rank,
    scores.pp as pp,
    scores.accuracy,
    scores.beatmap_id as beatmap_id,
    scores.beatmapset_id as beatmapset_id,
    bmap.title as beatmap_title,
    bmap.artist as beatmap_artist,
    bmap.version as beatmap_version
from
    (select * from Ainu.scores where userid = {0} and completed = 3 and play_mode = {1} and beatmap_id != 0 and pp >= 1 order by pp desc limit {2}) as scores
left join
    (select title, artist, version, beatmap_id, beatmapset_id from Ainu.beatmaps order by beatmap_id) as bmap on bmap.beatmap_id = scores.beatmap_id
order by pp desc;