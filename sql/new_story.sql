INSERT INTO `story` (diagnosis, reg_date, story_doctor, story_ward, story_patient)
            VALUES("$diagnosis", CURDATE(), $story_doctor, $story_ward, $story_patient)