CREATE TABLE devices(
    id SERIAL PRIMARY KEY,
    articleNumber VARCHAR UNIQUE,
    category VARCHAR, 
    subcategory VARCHAR,
    name VARCHAR,
    quantity BIGINT,
    productionYear INT,
    accountingYear INT,
    location VARCHAR(255),
    ownership VARCHAR(255),
    photo VARCHAR);
    
--I mean, we can create another table with categories
--So there won't be any naming duplicates
--But it's harder to modify specific item, so I'll leave it be in terms of flexibility

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    userid BIGINT UNIQUE,
    role BIGINT);

CREATE TABLE problematicDevices(
    id SERIAL PRIMARY KEY,
    status BOOLEAN,
    articleNumber VARCHAR UNIQUE REFERENCES devices(articleNumber),
    problemDescription VARCHAR,
    solutionDescription VARCHAR,
    photo VARCHAR,
    document VARCHAR,
    userid BIGINT REFERENCES users(userid));

CREATE TABLE notes(
    id SERIAL PRIMARY KEY,
    userid BIGINT REFERENCES users(userid),
    header VARCHAR,
    description VARCHAR);

CREATE TABLE software(
    id SERIAL PRIMARY KEY,
    userid BIGINT REFERENCES users(userid),
    filename VARCHAR,
    description VARCHAR);