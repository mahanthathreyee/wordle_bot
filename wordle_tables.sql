-- User and Role Creation
CREATE GROUP wordle_group;
CREATE USER wordle_bot PASSWORD 'abcd1234' IN GROUP wordle_group;

-- Database Restrictions
REVOKE ALL ON DATABASE wordle FROM public;              -- restrict access to database from the general public
GRANT CONNECT ON DATABASE wordle TO wordle_group;       -- Allow access for wordle_group to database

GRANT pg_read_all_data TO wordle_group;
GRANT pg_write_all_data TO wordle_group;

CREATE TABLE prefix_info_gain (
    id          SERIAL PRIMARY KEY,
    prefix      VARCHAR(255) UNIQUE,
    word        VARCHAR(255) NOT NULL,
    info_gain   FLOAT NOT NULL
);
