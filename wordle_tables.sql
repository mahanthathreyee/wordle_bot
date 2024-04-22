CREATE TABLE information_gain (
    id             SERIAL PRIMARY KEY,
    word           VARCHAR(255) UNIQUE NOT NULL,
    info_gain      FLOAT NOT NULL,
    parent_id      INTEGER NULL,
    info_level     INTEGER NOT NULL,

    FOREIGN KEY (parent_id) REFERENCES information_gain(id)
);
