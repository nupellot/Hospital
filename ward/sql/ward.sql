SELECT department.*, ward.*, story.*, patient.*, doctor.name AS doctor_name, doctor.surname AS doctor_surname, doctor.patronymic AS doctor_patronymic
FROM department JOIN ward ON wards_department=id_department JOIN story ON story_ward=id_ward JOIN patient ON story_patient=id_patient JOIN doctor ON id_doctor=story_doctor
WHERE discharge_date IS NULL AND id_ward=$id_ward AND id_department=$id_department
ORDER BY reg_date