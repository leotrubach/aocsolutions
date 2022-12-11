DROP SCHEMA IF EXISTS day03 CASCADE;
CREATE SCHEMA day03;

CREATE TABLE day03.inputs
(
    id   SERIAL,
    line TEXT NOT NULL
);

\COPY day03.inputs (line) FROM 'input.txt';

WITH codes as (SELECT id,
                      ARRAY(SELECT CASE
                                       WHEN ascii(t2.c) BETWEEN ascii('a') and ascii('z')
                                           THEN ascii(t2.c) - ascii('a') + 1
                                       WHEN ascii(t2.c) BETWEEN ascii('A') and ascii('Z')
                                           THEN ascii(t2.c) - ascii('A') + 27
                                       END
                            FROM (SELECT unnest(string_to_array(line, NULL)) as c) t2) code_list
               FROM day03.inputs),
     halves as (SELECT code_list[:array_length(code_list, 1) / 2]     as lh,
                       code_list[array_length(code_list, 1) / 2 + 1:] as rh
                FROM codes),
     solution1 as (SELECT SUM(v)
                   FROM (SELECT unnest(arr) v
                         FROM (SELECT ARRAY(SELECT unnest(halves.lh) INTERSECT SELECT unnest(halves.rh))
                                          arr
                               FROM halves) sol1) sol11),
     by_groups as (SELECT (id - 1) / 3 + 1 as gid, json_agg(code_list) cl
                   FROM codes
                   GROUP BY gid),
     flattened as (SELECT gid,
                          array(SELECT json_array_elements_text(cl -> 0))::int4[] as cl1,
                          array(SELECT json_array_elements_text(cl -> 1))::int4[] as cl2,
                          array(SELECT json_array_elements_text(cl -> 2))::int4[] as cl3
                   FROM by_groups)
     ,
     solution2 as (SELECT SUM(v)
                   FROM (SELECT unnest(arr) v
                         FROM (SELECT ARRAY(SELECT unnest(cl1)
                                            INTERSECT
                                            SELECT unnest(cl2)
                                            INTERSECT
                                            SELECT unnest(cl3)) arr
                               FROM flattened) sol2) sol21)
SELECT *
FROM solution1
UNION ALL
SELECT *
FROM solution2
