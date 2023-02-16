SELECT survey_story, survey.*, doctor.*
FROM patient JOIN story ON story_patient=id_patient JOIN survey ON survey_story=id_story JOIN doctor ON survey_doctor=id_doctor
WHERE patient.login="$login"