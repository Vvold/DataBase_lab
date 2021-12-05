BEGIN;


CREATE TABLE IF NOT EXISTS customer
(
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    subscription boolean
);

CREATE TABLE IF NOT EXISTS customer_library
(
id integer NOT NULL,
start_date integer NOT NULL
    customer_id integer NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_library_songs
(
    id integer NOT NULL,
customer_id integer NOT NULL,
customer_id integer NOT NULL
);

CREATE TABLE IF NOT EXISTS song
(
    id integer NOT NULL,
    address character varying(255) NOT NULL,
    manager_name character varying(50) NOT NULL,
    manager_surname character varying(150) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS song_photo
(
    id integer NOT NULL,
    author character varying(255) NOT NULL,
    album character varying(255) NOT NULL,
name character varying(255) NOT NULL,
duration integer NOT NULL,
year_of_release integer NOT NULL
    PRIMARY KEY (id)
);


ALTER TABLE customer_library
    ADD FOREIGN KEY (customer_id)
    REFERENCES customer (id)
    NOT VALID;


ALTER TABLE customer_library_songs
    ADD FOREIGN KEY (library_id)
    REFERENCES customer_library (id)
    NOT VALID;


ALTER TABLE customer_library_songs
    ADD FOREIGN KEY (song_id)
    REFERENCES song (id)
NOT VALID;

ALTER TABLE song_photo
    ADD FOREIGN KEY (song_id)
    REFERENCES song (id)
    NOT VALID;

END;