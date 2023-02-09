SELECT patient.*, story.*
FROM patient JOIN story ON patient.id_patient = story.story_patient
WHERE login = "$login"
ORDER BY reg_date DESC