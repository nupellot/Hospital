SELECT id_department, id_ward
FROM story JOIN ward ON story_ward=id_ward JOIN department ON wards_department=id_department
WHERE story_patient="$id_patient" AND discharge_date IS NULL