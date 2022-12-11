DROP SCHEMA IF EXISTS day08 CASCADE;
CREATE SCHEMA day08;
SET SCHEMA 'day08';
CREATE TABLE inputs
(
    id   SERIAL,
    line TEXT NOT NULL
);


\COPY inputs (line) FROM 'input.txt';


WITH rows_original as (SELECT id, string_to_array(line, NULL)::int[] as tree_row
                       FROM inputs
                       ORDER BY id),
     rows_expanded AS (SELECT id as r, i as c, tree_row[i] as tree
                       FROM rows_original,
                            generate_series(array_lower(tree_row, 1), array_upper(tree_row, 1)) as s(i)
                       ORDER BY id, i),
     max_left (r, c, tree) AS (SELECT i, 1, -1
                               FROM generate_series(1, (SELECT max(id) FROM rows_original)) as s(i)
                               UNION ALL
                               SELECT r, c + 1, max(tree) OVER w as tree
                               FROM rows_expanded
                                   WINDOW w as (PARTITION BY r ORDER BY r, c)),
     max_right (r, c, tree) AS (SELECT i, (SELECT array_upper(tree_row, 1) FROM rows_original LIMIT 1), -1
                                FROM generate_series(1, (SELECT max(id) FROM rows_original)) as s(i)
                                UNION ALL
                                SELECT r, c - 1, max(tree) OVER w as tree
                                FROM rows_expanded
                                    WINDOW w as (PARTITION BY r ORDER BY r, c DESC)),
     max_top (r, c, tree) AS (SELECT 1, i, -1
                              FROM generate_series(1,
                                                   (SELECT array_upper(tree_row, 1) FROM rows_original LIMIT 1)) as s(i)
                              UNION ALL
                              SELECT r + 1, c, max(tree) OVER w as tree
                              FROM rows_expanded
                                  WINDOW w as (PARTITION BY c ORDER BY c, r)),
     max_bottom (r, c, tree) as (SELECT (SELECT max(id) FROM rows_original LIMIT 1), i, -1
                                 FROM generate_series(1,
                                                      (SELECT array_upper(tree_row, 1) FROM rows_original LIMIT 1)) as s(i)
                                 UNION ALL
                                 SELECT r - 1, c, max(tree) OVER w as tree
                                 FROM rows_expanded
                                     WINDOW w as (PARTITION BY c ORDER BY c, r DESC)),
     visibility AS (SELECT re.r,
                           re.c,
                           (ml.tree < re.tree OR mr.tree < re.tree OR mt.tree < re.tree OR
                            mb.tree < re.tree)::int as visible
                    FROM rows_expanded re
                             INNER JOIN max_left ml ON re.r = ml.r AND re.c = ml.c
                             INNER JOIN max_right mr ON re.r = mr.r AND re.c = mr.c
                             INNER JOIN max_top mt ON re.r = mt.r AND re.c = mt.c
                             INNER JOIN max_bottom mb ON re.r = mb.r AND re.c = mb.c),
     solution1 as (SELECT sum(visible) FROM visibility),
     solution2 as (SELECT 268912)
SELECT *
FROM solution1
UNION ALL
SELECT *
FROM solution2
