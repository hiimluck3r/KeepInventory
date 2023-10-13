CREATE TABLE devices(
    id SERIAL PRIMARY KEY,
    articleNumber BIGINT UNIQUE,
    category VARCHAR,
    subcategory VARCHAR,
    name VARCHAR,
    quantity BIGINT,
    productionYear INT,
    accountingYear INT,
    location VARCHAR(255),
    ownership VARCHAR(255),
    photo VARCHAR);

CREATE TABLE problematicDevices(
    id SERIAL PRIMARY KEY,
    status BOOLEAN,
    articleNumber BIGINT UNIQUE,
    problemDescription VARCHAR,
    solutionDescription VARCHAR,
    photo VARCHAR,
    document VARCHAR,
    userid BIGINT);

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    userid BIGINT UNIQUE,
    role VARCHAR(8));

CREATE TABLE notes(
    id SERIAL PRIMARY KEY,
    userid BIGINT,
    header VARCHAR,
    description VARCHAR);

CREATE TABLE software(
    id SERIAL PRIMARY KEY,
    userid BIGINT,
    filename VARCHAR,
    description VARCHAR);