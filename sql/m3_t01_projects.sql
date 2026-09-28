-- # 新增：M3-T01 PostgreSQL / SQL CRUD 练习

CREATE TABLE m3_t01_projects (
    name TEXT NOT NULL,
    description TEXT
);

INSERT INTO m3_t01_projects (name, description)
VALUES ('alpha', 'First PostgreSQL project');

INSERT INTO m3_t01_projects (name, description)
VALUES ('beta', 'Second PostgreSQL project');

SELECT name, description
FROM m3_t01_projects
ORDER BY name;

UPDATE m3_t01_projects
SET description = 'Alpha updated in PostgreSQL'
WHERE name = 'alpha';

SELECT name, description
FROM m3_t01_projects
WHERE name = 'alpha';

DELETE FROM m3_t01_projects
WHERE name = 'beta';

SELECT name, description
FROM m3_t01_projects
ORDER BY name;
