SELECT count(id_patient) AS "amount"
FROM department JOIN ward ON wards_department=id_department JOIN story ON story_ward=id_ward JOIN patient ON story_patient=id_patient
WHERE discharge_date IS NULL AND id_ward=$id_ward AND id_department=$id_department
GROUP BY id_ward