DROP SCHEMA IF EXISTS day04 CASCADE;
CREATE SCHEMA day04;

CREATE TABLE day04.inputs (
  line TEXT NOT NULL
);

\COPY day01.inputs (line) FROM 'input.txt';

WITH partial AS (
    SELECT string_to_array(line, ',') ar
    FROM day01.inputs
),
parsed as (
    SELECT string_to_array(ar[1], '-') pr1, string_to_array(ar[2], '-') pr2
    FROM partial
),
ranges as (
    SELECT int4range(pr1[1]::int, pr1[2]::int, '[]') fr,
           int4range(pr2[1]::int, pr2[2]::int, '[]') sr
    FROM parsed
),
solution as (
    SELECT COUNT(*) FROM ranges WHERE fr @> sr OR sr @> fr
    UNION ALL
    SELECT COUNT(*) FROM ranges WHERE fr && sr
)

SELECT * FROM solution

