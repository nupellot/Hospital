SELECT story.*, doctor.image, doctor.surname, doctor.name, doctor.patronymic, doctor.login, id_ward, id_department
FROM patient JOIN story ON story_patient=id_patient JOIN doctor ON story_doctor=id_doctor JOIN ward ON id_ward=story_ward JOIN department ON wards_department=id_department
WHERE patient.login="$login"
ORDER BY reg_date DESC