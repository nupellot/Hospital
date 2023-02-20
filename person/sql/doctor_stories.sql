select distinct * from (
    SELECT story.*, doctor.*, patient.image AS "patient_image", patient.name AS "patient_name", patient.surname AS "patient_surname", patient.patronymic AS "patient_patronymic", ward.*, department.*
    from story JOIN doctor ON story_doctor=id_doctor JOIN patient ON story_patient=id_patient JOIN ward ON id_ward=story_ward JOIN department ON wards_department=id_department
    WHERE story_doctor = $doctor_id
union
    SELECT story.*, doctor.*, patient.image AS "patient_image", patient.name AS "patient_name", patient.surname AS "patient_surname", patient.patronymic AS "patient_patronymic", ward.*, department.*
    from survey join story on survey_story = id_story JOIN doctor ON story_doctor=id_doctor JOIN patient ON story_patient=id_patient JOIN ward ON id_ward=story_ward JOIN department ON wards_department=id_department
    WHERE survey_doctor = $doctor_id
) as temp
ORDER BY discharge_date ASC