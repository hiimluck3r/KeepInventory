CREATE TABLE inventory(
    id SERIAL PRIMARY KEY,
    group VARCHAR,
    subgroup VARCHAR,
    title VARCHAR,
    quantity BIGINT,
    serialkey BIGINT,
    recordyear INT,
    helder VARCHAR,
    releaseyear INT,
    cabinet VARCHAR);

COPY inventory(group, subgroup, title, quantity, serialkey, recordyear, helder, releaseyear, cabinet) FROM '/docker-entrypoint-initdb.d/data.csv' DELIMITER ',' CSV HEADER;