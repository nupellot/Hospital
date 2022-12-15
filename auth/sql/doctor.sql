SELECT doctor.*, YEAR(CURDATE()) - YEAR(recruitment_date) AS "experience"
FROM doctor
WHERE login = "$login" AND password = "$password"