UPDATE story
SET discharge_date = CURDATE()
WHERE story_patient=$patient_id