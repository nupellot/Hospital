SELECT department.id_department, ward.id_ward, wtype, capacity, ward_occupancy
FROM department
JOIN ward ON wards_department=id_department LEFT JOIN
	(SELECT id_department, id_ward, count(id_patient) AS "ward_occupancy"
    FROM department JOIN ward ON wards_department=id_department JOIN story ON story_ward=id_ward JOIN patient ON story_patient=id_patient JOIN doctor ON id_doctor=story_doctor
	WHERE discharge_date IS NULL
    GROUP BY id_ward
    ORDER BY id_department, id_ward)
    AS temp ON temp.id_department=department.id_department AND temp.id_ward=ward.id_ward
ORDER BY id_ward