CREATE TABLE users(
    id INTEGER PRIMARY KEY generated always as IDENTITY,
    userid BIGINT UNIQUE,
    role SMALLINT);

CREATE TABLE devices(
    id INTEGER PRIMARY KEY generated always as IDENTITY,
    articleNumber VARCHAR UNIQUE,
    category VARCHAR, 
    subcategory VARCHAR,
    name VARCHAR(255),
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
    articleNumber VARCHAR UNIQUE REFERENCES devices(articleNumber)
    ON DELETE CASCADE ON UPDATE CASCADE,
    problemDescription VARCHAR,
    solutionDescription VARCHAR,
    photo VARCHAR,
    document VARCHAR,
    userid BIGINT REFERENCES users(userid));

CREATE TABLE notes(
    id INTEGER PRIMARY KEY generated always as IDENTITY,
    userid BIGINT REFERENCES users(userid),
    header VARCHAR,
    description VARCHAR);

CREATE TABLE software(
    id INTEGER PRIMARY KEY generated always as IDENTITY,
    userid BIGINT REFERENCES users(userid),
    filename VARCHAR,
    description VARCHAR);