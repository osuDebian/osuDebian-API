SELECT 
	userdata.id, username, username_aka, sub.country, ifnull(is_verified,0) as is_verified, pp, total_score, ranked_score, replays_watched, total_hits, playtime, round(accuracy, 2) as accuracy, maximum_combo, playcount, ifnull(rank_xh, 0) as rank_xh, ifnull(rank_x, 0) as rank_x, ifnull(rank_sh, 0) as rank_sh, ifnull(rank_s, 0) as rank_s, ifnull(rank_a, 0) as rank_a, ifnull(rank_b, 0) as rank_b, ifnull(rank_c, 0) as rank_c
FROM
    (select id, username, username_aka, pp_{1} as pp, total_score_{1} as total_score, ranked_score_{1} as ranked_score, replays_watched_{1} as replays_watched, total_hits_{1} as total_hits, playtime_{1} as playtime, avg_accuracy_{1} as accuracy from Ainu.rx_stats where id = {0}) as userdata
left join
	(select Count(id) as playcount, userid from Ainu.scores_relax where userid = {0}) as playcounts on playcounts.userid = userdata.id
left join
	(select id, country from Ainu.users_stats where id = {0}) as sub on sub.id = userdata.id
left join
	(select Count(rank) as rank_xh, userid from Ainu.scores_relax where userid = {0} and rank = 'XH') as rank_xh on rank_xh.userid = userdata.id
left join
	(select Count(rank) as rank_x, userid from Ainu.scores_relax where userid = {0} and rank = 'X') as rank_x on rank_x.userid = userdata.id
left join
	(select Count(rank) as rank_sh, userid from Ainu.scores_relax where userid = {0} and rank = 'SH') as rank_sh on rank_sh.userid = userdata.id
left join
	(select Count(rank) as rank_s, userid from Ainu.scores_relax where userid = {0} and rank = 'S') as rank_s on rank_s.userid = userdata.id
left join
	(select Count(rank) as rank_a, userid from Ainu.scores_relax where userid = {0} and rank = 'A') as rank_a on rank_a.userid = userdata.id
left join
	(select Count(rank) as rank_b, userid from Ainu.scores_relax where userid = {0} and rank = 'B') as rank_b on rank_b.userid = userdata.id
left join
	(select Count(rank) as rank_c, userid from Ainu.scores_relax where userid = {0} and rank = 'C') as rank_c on rank_c.userid = userdata.id
left join
	(select max(max_combo) as maximum_combo, userid from Ainu.scores_relax where userid = {0} and completed = 3) as maxcombo on maxcombo.userid = userdata.id
left join
	(select is_verified, id from Ainu.users where id = {0}) as usersdata on usersdata.id = userdata.id
;