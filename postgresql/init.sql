CREATE TABLE users(
    id INTEGER UNIQUE generated always as IDENTITY,
    userid BIGINT PRIMARY KEY,
    role SMALLINT);

CREATE TABLE devices(
    id INTEGER UNIQUE generated always as IDENTITY,
    articleNumber VARCHAR PRIMARY KEY,
    category VARCHAR, 
    subcategory VARCHAR,
    name VARCHAR,
    quantity BIGINT,
    productionYear SMALLINT,
    accountingYear SMALLINT,
    location VARCHAR(255),
    ownership VARCHAR(255),
    photo VARCHAR);

--I mean, we can create another table with categories
--So there won't be any naming duplicates
--But it's harder to modify specific item, so I'll leave it be in terms of flexibility

CREATE TABLE problematicDevices(
    id INTEGER PRIMARY KEY generated always as IDENTITY,
    status BOOLEAN,
    articleNumber VARCHAR UNIQUE NOT NULL REFERENCES devices(articleNumber)
    ON DELETE CASCADE ON UPDATE CASCADE,
    problemDescription VARCHAR,
    solutionDescription VARCHAR,
    userid BIGINT REFERENCES users(userid) ON DELETE SET NULL);

CREATE TABLE notes(
    id INTEGER PRIMARY KEY generated always as IDENTITY,
    userid BIGINT REFERENCES users(userid) ON DELETE SET NULL,
    header VARCHAR,
    description VARCHAR);

CREATE TABLE software(
    id INTEGER PRIMARY KEY generated always as IDENTITY,
    userid BIGINT REFERENCES users(userid) ON DELETE SET NULL,
    filename VARCHAR,
    fileurl VARCHAR,
    description VARCHAR);
