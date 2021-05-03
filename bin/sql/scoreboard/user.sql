SELECT SQL_CACHE json_object(
	'username',username, 
	'userid',id 
) as data
FROM users WHERE username like '{0}';