CREATE TABLE users(
    email TEXT UNIQUE NOT NULL PRIMARY KEY,
    passwordHash TEXT
);
CREATE TABLE FDA_Data(
    event_id INTEGER PRIMARY KEY,
    recalling_firm TEXT,
    distribution_pattern TEXT,
    product_description TEXT,
    product_quantity TEXT,
    reason_for_recall TEXT,
    recall_initiation_date INTEGER,
    status TEXT
);