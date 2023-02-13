SELECT id_department, id_ward, count(id_patient) AS "ward_occupancy", capacity
FROM department JOIN ward ON wards_department=id_department JOIN story ON story_ward=id_ward JOIN patient ON story_patient=id_patient
WHERE discharge_date IS NULL
GROUP BY id_ward
ORDER BY id_ward