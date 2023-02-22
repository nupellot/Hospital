SELECT story.*
FROM story
WHERE story_patient = $patient_id AND discharge_date IS NULL
LIMIT 1