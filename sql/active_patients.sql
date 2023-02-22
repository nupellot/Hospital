SELECT patient.surname, patient.name, patient.patronymic, patient.id_patient, department.id_department,  ward.id_ward, story.*
FROM patient JOIN story ON story_patient=id_patient JOIN ward ON story_ward=id_ward JOIN department ON wards_department=id_department
WHERE discharge_date IS NULL
ORDER BY reg_date DESC