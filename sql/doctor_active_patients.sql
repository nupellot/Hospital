SELECT *
FROM story JOIN patient ON story_patient=id_patient JOIN ward ON id_ward=story_ward JOIN department ON wards_department=id_department
WHERE discharge_date IS NULL AND story_doctor=$id_doctor
ORDER BY reg_date DESC