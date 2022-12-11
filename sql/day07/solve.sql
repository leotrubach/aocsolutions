DROP SCHEMA IF EXISTS day07 CASCADE;
CREATE SCHEMA day07;
SET SCHEMA 'day07';
CREATE TABLE inputs
(
    id   SERIAL,
    line TEXT NOT NULL
);


\COPY inputs (line) FROM 'input.txt';


WITH RECURSIVE
    marked as (SELECT id, (substring(line, 1, 1) = '$')::int as is_command, line
               FROM inputs
               ORDER BY id),
    commands_numbered as (SELECT id, is_command::boolean, sum(is_command) OVER (ORDER BY id) as command_id, line
                          FROM marked),
    commands_extracted as (SELECT id, command_id, (string_to_array(line, ' '))[2] as command_type, line
                           FROM commands_numbered
                           WHERE is_command IS TRUE),
    commands_with_params as (SELECT id,
                                    command_id,
                                    command_type,
                                    CASE
                                        WHEN command_type = 'cd' THEN (string_to_array(line, ' '))[3]
                                        END as param
                             FROM commands_extracted),
    command_paths (cmd_number, cur_path) as (SELECT 0, ARRAY []::text[]
                                             UNION ALL
                                             SELECT fs.cmd_number + 1,
                                                    CASE
                                                        WHEN ca.command_type = 'cd' THEN
                                                            CASE
                                                                WHEN ca.param = '/' THEN '{}'::text[]
                                                                WHEN ca.param = '..'
                                                                    THEN fs.cur_path[:array_length(fs.cur_path, 1) - 1]
                                                                ELSE fs.cur_path || ARRAY [ca.param]
                                                                END
                                                        ELSE fs.cur_path
                                                        END as cur_path
                                             FROM command_paths fs
                                                      JOIN commands_with_params ca ON fs.cmd_number + 1 = ca.command_id
                                             WHERE fs.cmd_number < (SELECT max(command_id) FROM commands_with_params)),
    cmd_paths_str AS (SELECT cmd_number, array_to_string(cur_path, '/') || '/' as path
                      FROM command_paths),
    ls_outputs AS (SELECT cn.id, cn.command_id, (string_to_array(cn.line, ' '))[1]::int as fsize
                   FROM commands_numbered cn
                   WHERE cn.command_id IN (SELECT command_id FROM commands_with_params WHERE command_type = 'ls')
                     AND cn.is_command IS FALSE
                     AND substring(cn.line, 1, 3) != 'dir'),
    file_aggs AS (SELECT command_id, SUM(fsize) as total_size
                  FROM ls_outputs
                  GROUP BY command_id),
    folder_sizes AS (SELECT cps.cur_path path, fa.total_size
                     FROM command_paths cps
                              JOIN file_aggs fa ON cps.cmd_number = fa.command_id
                     ORDER BY array_length(cps.cur_path, 1) DESC, cps.cur_path),
    folder_total_size as (SELECT jsonb_array_elements(((SELECT jsonb_agg(fs.path[1:ai])
                                          FROM generate_series(0, array_length(fs.path, 1)) ai))) path,
                                 fs.total_size
                          FROM folder_sizes fs),
    folder_aggs as (
        SELECT path, sum(total_size) total_size
        FROM folder_total_size
        GROUP BY path
    ),
    solution1 AS (
        SELECT sum(total_size)
        FROM folder_aggs
        WHERE total_size < 100000
    ),
    solution2 as (
        SELECT total_size
               FROM folder_aggs WHERE total_size > (SELECT total_size FROM folder_aggs WHERE path = '[]'::jsonb) - (70000000 - 30000000)
                                           ORDER BY total_size
                                           FETCH FIRST 1 ROWS ONLY
    )
SELECT * FROM solution1
UNION ALL
SELECT * FROM solution2