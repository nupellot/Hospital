SELECT *
from survey JOIN doctor ON survey_doctor = id_doctor
where survey_story in $story_ids

