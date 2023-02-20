SELECT *, department_name
FROM doctor LEFT JOIN department ON id_department=doctors_department
WHERE login = "$login"