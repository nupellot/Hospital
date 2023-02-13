SELECT id_department, department_name, id_head, floor, department_occupancy, sum(capacity) AS department_capacity
FROM department JOIN ward ON wards_department=id_department JOIN
		(SELECT count(id_story) AS department_occupancy, id_department
		FROM story JOIN ward ON story_ward=id_ward JOIN department ON id_department = wards_department
        WHERE discharge_date IS NULL
        GROUP BY id_department)
        AS tmp USING(id_department)
GROUP BY id_department
ORDER BY id_department

# Для каждого отделения из результирующей таблицы запустишь запрос из файла departments_wards.sql, передавая туда  id_department из строки этой таблицы