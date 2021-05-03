select SQL_CACHE json_arrayagg( 
        json_object(
			'scoreid',id, 
			'userid',userid, 
			'username',username, 
			'country',country, 
			'score',score, 
			'rank',rank, 
			'max_combo',max_combo, 
			'mods',mods, 
			'count300',`300_count`, 
			'count100',`100_count`, 
			'count50',`50_count`, 
			'countmiss',misses_count, 
			'time',time, 
			'play_mode',play_mode, 
			'accuracy',accuracy, 
			'score',Format(score, 0), 
			'pp',pp, 
			'fc',fc 
        ) ORDER BY {2} DESC
) as data
from(
	select score.id, score.userid, users.username, userstat.country, score.score, score.rank, score.max_combo, score.mods, score.`300_count`, score.`100_count`, score.`50_count`, score.misses_count, score.time, score.play_mode, score.accuracy, Format(score.score, 0), score.pp, combo.fc
	from(select id,username, ban_datetime from users where ban_datetime = 0) as users 
	join (select id, country from users_stats) as userstat on userstat.id = users.id 
	join (SELECT * FROM {3} WHERE beatmap_md5 = '{0}' AND completed = 3 ORDER BY {2} DESC) as score on score.userid = users.id 
	left join (select max_combo as fc ,beatmap_md5 from beatmaps where beatmap_md5 = '{0}') as combo on score.beatmap_md5 = combo.beatmap_md5 
	WHERE play_mode = {1} order by score.{2} desc
) AS xx;