-- User and Role Creation
CREATE GROUP wordle_group;
CREATE USER wordle_bot PASSWORD 'abcd1234' IN GROUP wordle_group;

-- Database Restrictions
REVOKE ALL ON DATABASE wordle FROM public;              -- restrict access to database from the general public
GRANT CONNECT ON DATABASE wordle TO wordle_group;       -- Allow access for wordle_group to database

GRANT pg_read_all_data TO wordle_group;
GRANT pg_write_all_data TO wordle_group;

CREATE TABLE first_level_info_gain (
    id          SERIAL PRIMARY KEY,
    word        VARCHAR(255) UNIQUE NOT NULL,
    info_gain   FLOAT NOT NULL
);

CREATE TABLE second_level_info_gain (
    id          SERIAL PRIMARY KEY,
    word        VARCHAR(255) UNIQUE NOT NULL,
    info_gain   FLOAT NOT NULL,
    parent_id   INT NOT NULL REFERENCES first_level_info_gain (id)
);

CREATE INDEX second_word_parent_index ON second_level_info_gain (parent_id);

CREATE TABLE second_level_word_status (
    word_id     INT PRIMARY KEY NOT NULL REFERENCES first_level_info_gain(id),
    word_status BOOLEAN DEFAULT FALSE
);
