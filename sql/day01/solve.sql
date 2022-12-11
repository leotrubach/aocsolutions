DROP SCHEMA IF EXISTS day01 CASCADE;
CREATE SCHEMA day01;
SET SCHEMA 'day01';
CREATE TABLE inputs
(
    id   SERIAL,
    line TEXT NOT NULL
);

\COPY inputs (line) FROM 'input.txt';

WITH parsed as (
    SELECT id,
           CASE WHEN length(line) > 0 THEN line::int END as value
    FROM inputs
),
    marked as (
        SELECT id, value, (value IS NULL)::int as mark
        FROM parsed
    ),
    grouped as (
        SELECT id, value, sum(mark) OVER (ORDER BY id) as group_id
        FROM marked
    ),
    totals AS (
        SELECT SUM(value) as total_consumption FROM grouped
                          GROUP BY group_id
    ),
    solution1 AS (
        SELECT max(total_consumption)
        FROM totals
    ),
    rows2 AS (
        SELECT total_consumption
        FROM totals
        ORDER BY total_consumption DESC
        FETCH FIRST 3 ROWS ONLY
    ),
    solution2 AS (
        SELECT SUM(total_consumption) FROM rows2
    )
SELECT * FROM solution1
UNION ALL
SELECT * FROM solution2
