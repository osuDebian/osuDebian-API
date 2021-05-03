select
	name, description, icon, version as category, mode, if(userachiev.user_id = {0}, 1, 0) as enabled, time
from
	(select * from Ainu.achievements where mode = {1} order by id asc) as alls
left join 
	(select user_id, achievement_id, time from Ainu.users_achievements where user_id = {0}) as userachiev on alls.id = userachiev.achievement_id
order by id asc
;