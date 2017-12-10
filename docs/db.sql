CREATE TABLE items(
	id SERIAL PRIMARY KEY,
	date int NOT NULL,
	latitude NUMERIC NOT NULL,
	longitude NUMERIC NOT NULL	
);


CREATE OR REPLACE FUNCTION get_items(limit_num numeric=100)
    RETURNS TABLE(if int, date int, latitude text, longitude text) AS
    $BODY$
         SELECT
	        id AS id,
	        date AS date,
	        trim(to_char(latitude, '99D9999999')) AS latitude,
	        trim(to_char(longitude, '99D9999999')) AS longitude
	    FROM items
	    ORDER BY date DESC
	    LIMIT limit_num;
    $BODY$
    LANGUAGE sql;


CREATE OR REPLACE FUNCTION add_item(date INT, latitude NUMERIC, longitude NUMERIC) 
    RETURNS void AS
    $BODY$
    	INSERT INTO items(date, latitude, longitude) 
    	VALUES (date, latitude, longitude);
    $BODY$
    LANGUAGE sql;
