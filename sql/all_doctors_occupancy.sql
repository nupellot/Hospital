SELECT doctor.id_doctor, count(id_story) AS "occupancy"
FROM doctor JOIN story ON story_doctor=id_doctor
WHERE discharge_date IS NULL
GROUP BY id_doctor
ORDER BY surname