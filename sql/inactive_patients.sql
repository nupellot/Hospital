SELECT
    *, YEAR(birth_date) AS "birth_year"
FROM
    patient
WHERE
    id_patient NOT IN (SELECT
            id_patient
        FROM
            patient
                JOIN
            story ON story_patient = id_patient
        WHERE
            discharge_date IS NULL
        ORDER BY reg_date DESC)