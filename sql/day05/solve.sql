DROP SCHEMA IF EXISTS day05 CASCADE;
CREATE SCHEMA day05;
SET SCHEMA 'day05';
CREATE TABLE inputs
(
    id   SERIAL,
    line TEXT NOT NULL
);

--CREATE TABLE cargo(id int, cargo_id int, content text);
--CREATE TABLE commands (id int, amount int, src int, dst int);

\COPY inputs (line) FROM 'input.txt';


WITH RECURSIVE
    empty_line_id AS (SELECT id
                      FROM inputs
                      WHERE line = ''
                      LIMIT 1),
    cargo_raw AS (SELECT id, line
                  FROM inputs
                  WHERE id < (SELECT id from empty_line_id)),
    cargo_untrim AS (SELECT id, rpad(line, (SELECT max(length(line)) FROM cargo_raw)) as line
                     FROM cargo_raw),
    cargo_numbers AS (SELECT regexp_split_to_table(trim(line), E'\\s+')::int cargo_id
                      FROM cargo_untrim
                      WHERE id = (select max(id) FROM cargo_untrim)),
    cargo_buckets_raw AS (SELECT id, line
                          FROM cargo_untrim
                          WHERE id < (select max(id) FROM cargo_untrim)),
    cargo_table_decomposed AS (SELECT cbr.id, cn.cargo_id, substr(line, 4 * (cn.cargo_id - 1) + 2, 1) as content
                               FROM cargo_buckets_raw cbr,
                                    cargo_numbers cn),
    cargo_table_cleaned AS (SELECT *
                            FROM cargo_table_decomposed
                            WHERE content != ' '
                            ORDER BY cargo_id, id DESC),
    cargo_table as (SELECT row_number() over w as id, cargo_id, content
                    FROM cargo_table_cleaned
                        WINDOW w AS (PARTITION BY cargo_id ORDER BY id DESC)),
    cargo_json_rows as (SELECT cargo_id, json_agg(content ORDER BY id) boxes
                        FROM cargo_table
                        GROUP BY cargo_id),
    cargo_json as (SELECT jsonb_object_agg(cargo_id, boxes) state
                   FROM cargo_json_rows),
    commands_raw as (SELECT id, string_to_array(line, ' ') as arr
                     FROM inputs
                     WHERE id > (SELECT id FROM empty_line_id)),
    commands AS (SELECT row_number() over (ORDER BY id) as id,
                        arr[2]::int                     as amount,
                        arr[4]::int                     as src,
                        arr[6]::int                     as dest
                 FROM commands_raw),
    run1 (iteration_id, state) AS (SELECT 0, (SELECT state from cargo_json)
                                   UNION ALL
                                   (WITH pr as (SELECT *
                                                FROM run1
                                                         JOIN commands cmd ON cmd.id = run1.iteration_id + 1),
                                         to_move as (SELECT jsonb_path_query_array(
                                                                        pr.state -> cmd.src::text,
                                                                        ('$[' ||
                                                                         jsonb_array_length(pr.state -> cmd.src::text) -
                                                                         cmd.amount ||
                                                                         ' to ' ||
                                                                         jsonb_array_length(pr.state -> cmd.src::text) -
                                                                         1 ||
                                                                         ']')::jsonpath
                                                                ) as state
                                                     FROM pr
                                                              JOIN commands cmd on cmd.id = pr.iteration_id + 1),
                                         inverted as (SELECT (SELECT jsonb_agg(value ORDER BY ORDINALITY DESC)
                                                              FROM jsonb_array_elements(state) WITH ORDINALITY) as state
                                                      FROM to_move),
                                         to_remain as (SELECT jsonb_build_object(
                                                                      cmd.src,
                                                                      jsonb_path_query_array(
                                                                                  pr.state -> cmd.src::text,
                                                                                  ('$[' ||
                                                                                   0 ||
                                                                                   ' to ' ||
                                                                                   jsonb_array_length(pr.state -> cmd.src::text) -
                                                                                   cmd.amount - 1 ||
                                                                                   ']')::jsonpath
                                                                          )
                                                                  ) as state
                                                       FROM pr
                                                                JOIN commands cmd on cmd.id = pr.iteration_id + 1),
                                         to_append AS (SELECT jsonb_build_object(
                                                                      cmd.dest, (pr.state -> cmd.dest::text) ||
                                                                                (SELECT state FROM inverted)
                                                                  ) as state
                                                       FROM pr
                                                                JOIN commands cmd on cmd.id = pr.iteration_id + 1)
                                    SELECT pr.iteration_id + 1,
                                           pr.state || (select state from to_remain) || (select state from to_append)
                                    FROM pr
                                             JOIN commands cmd
                                                  ON cmd.id = pr.iteration_id + 1
                                    WHERE pr.iteration_id < (SELECT max(id) FROM commands))),
    run2 (iteration_id, state) AS (SELECT 0, (SELECT state from cargo_json)
                                   UNION ALL
                                   (WITH pr as (SELECT *
                                                FROM run2
                                                         JOIN commands cmd ON cmd.id = run2.iteration_id + 1),
                                         to_move as (SELECT jsonb_path_query_array(
                                                                        pr.state -> cmd.src::text,
                                                                        ('$[' ||
                                                                         jsonb_array_length(pr.state -> cmd.src::text) -
                                                                         cmd.amount ||
                                                                         ' to ' ||
                                                                         jsonb_array_length(pr.state -> cmd.src::text) -
                                                                         1 ||
                                                                         ']')::jsonpath
                                                                ) as state
                                                     FROM pr
                                                              JOIN commands cmd on cmd.id = pr.iteration_id + 1),
                                         to_remain as (SELECT jsonb_build_object(
                                                                      cmd.src,
                                                                      jsonb_path_query_array(
                                                                                  pr.state -> cmd.src::text,
                                                                                  ('$[' ||
                                                                                   0 ||
                                                                                   ' to ' ||
                                                                                   jsonb_array_length(pr.state -> cmd.src::text) -
                                                                                   cmd.amount - 1 ||
                                                                                   ']')::jsonpath
                                                                          )
                                                                  ) as state
                                                       FROM pr
                                                                JOIN commands cmd on cmd.id = pr.iteration_id + 1),
                                         to_append AS (SELECT jsonb_build_object(
                                                                      cmd.dest, (pr.state -> cmd.dest::text) ||
                                                                                (SELECT state FROM to_move)
                                                                  ) as state
                                                       FROM pr
                                                                JOIN commands cmd on cmd.id = pr.iteration_id + 1)
                                    SELECT pr.iteration_id + 1,
                                           pr.state || (select state from to_remain) || (select state from to_append)
                                    FROM pr
                                             JOIN commands cmd
                                                  ON cmd.id = pr.iteration_id + 1
                                    WHERE pr.iteration_id < (SELECT max(id) FROM commands))),
    solution1_chars AS (SELECT (state -> cn.cargo_id::text ->> -1) as c
                        FROM run1,
                             cargo_numbers cn
                        WHERE iteration_id = (SELECT max(id) FROM commands)
                        ORDER BY cn.cargo_id),
    solution1 AS (SELECT string_agg(c, '') as answer
                  FROM solution1_chars),
    solution2_chars AS (SELECT (state -> cn.cargo_id::text ->> -1) as c
                        FROM run2,
                             cargo_numbers cn
                        WHERE iteration_id = (SELECT max(id) FROM commands)
                        ORDER BY cn.cargo_id),
    solution2 AS (SELECT string_agg(c, '') as answer
                  FROM solution2_chars)
SELECT *
FROM solution1
UNION ALL
SELECT *
FROM solution2