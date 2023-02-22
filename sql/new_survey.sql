INSERT INTO `survey` (date, prescriptions, survey_doctor, survey_story)
VALUES(CURDATE(), "$prescriptions", $survey_doctor, $survey_story)