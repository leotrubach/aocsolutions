DROP SCHEMA IF EXISTS day02 CASCADE;
CREATE SCHEMA day02;
SET SCHEMA 'day02';
CREATE TABLE inputs
(
    id   SERIAL,
    line TEXT NOT NULL
);

\COPY inputs (line) FROM 'input.txt';

WITH split AS (
    SELECT id, string_to_array(line, ' ') parts
    FROM inputs
),
    parsed AS (
        SELECT id, parts[1] as first, parts[2] as second
        FROM split
    ),
    nums AS (
        SELECT id, ASCII(first) - ASCII('A') as first, ASCII(second) - ASCII('X') as second
        FROM parsed
    ),
    points1 AS (
        SELECT first + 1, second + 1, mod((second - first + 4), 3) * 3 + second + 1 as result
        FROM nums
    ),
    solution1 as (
        SELECT sum(result) FROM points1
    ),
    points2 as (
        SELECT first, second, mod((first + second + 2), 3) + 1 + second * 3 as result
        FROM nums
    ),
    solution2 as (
        SELECT sum(result) FROM points2
    )
SELECT * FROM solution1
UNION ALL
SELECT * FROM solution2
