SELECT id_department, doctor.*, count(id_story) AS "doctor_occupancy"
FROM department JOIN doctor ON department.id_department=doctor.doctors_department LEFT JOIN story ON story_doctor=id_doctor
WHERE discharge_date IS NULL
GROUP BY id_doctor
ORDER BY id_department, surname