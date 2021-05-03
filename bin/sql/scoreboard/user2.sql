SELECT SQL_CACHE json_object(
	'username',username, 
	'userid',id 
) as data FROM users_stats WHERE username like '{0}';