DROP SCHEMA IF EXISTS day06 CASCADE;
CREATE SCHEMA day06;
SET SCHEMA 'day06';
CREATE TABLE inputs
(
    id   SERIAL,
    line TEXT NOT NULL
);


\COPY inputs (line) FROM 'input.txt';

WITH by_chunks_of_four AS (
    SELECT generate_series as i, substring(line, generate_series.generate_series - 4 + 1, 4) chunk
    FROM inputs, generate_series(4, length(line))
),
    dedups_of_four AS (
        SELECT i, (SELECT array_agg(DISTINCT t.chunk) FROM (SELECT string_to_table(c4.chunk, NULL) chunk) t) as s4
        FROM by_chunks_of_four c4
    ),
    solution1 AS (
        SELECT min(df.i) as answer FROM dedups_of_four df WHERE array_length(df.s4, 1) = 4
    ),
    by_chunks_of_fourteen AS (
    SELECT generate_series as i, substring(line, generate_series.generate_series - 14 + 1, 14) chunk
    FROM inputs, generate_series(14, length(line))
),
    dedups_of_fourteen AS (
        SELECT i, (SELECT array_agg(DISTINCT t.chunk) FROM (SELECT string_to_table(c4.chunk, NULL) chunk) t) as s4
        FROM by_chunks_of_fourteen c4
    ),
    solution2 AS (
        SELECT min(df.i) as answer FROM dedups_of_fourteen df WHERE array_length(df.s4, 1) = 14
    )
SELECT * FROM solution1
UNION ALL
SELECT * FROM solution2