SELECT survey_story, survey.*
FROM patient JOIN story ON story_patient=id_patient JOIN survey ON survey_story=id_story
WHERE login="$login"