SELECT story.*
FROM patient JOIN story ON story_patient=id_patient
WHERE login="$login"