select user_id, user_group, user_name
from internal_user
where user_login = "$login" and user_password ="$password"
