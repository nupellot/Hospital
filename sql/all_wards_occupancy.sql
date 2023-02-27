SELECT id_ward, count(id_story) AS "occupancy"
FROM story JOIN ward ON story_ward=id_ward
WHERE discharge_date IS NULL
GROUP BY story_ward