CREATE TABLE items(
	id SERIAL PRIMARY KEY,
	date int NOT NULL,
	latitude NUMERIC NOT NULL,
	longitude NUMERIC NOT NULL	
);


CREATE OR REPLACE FUNCTION get_items(offset_val numeric=0, limit_val numeric=100)
    RETURNS TABLE(id int, date int, latitude numeric, longitude numeric) AS
    $BODY$
         SELECT
	        id AS id,
	        date AS date,
	        latitude AS latitude,
	        longitude AS longitude
	    FROM items
	    ORDER BY date DESC
	    OFFSET offset_val
	    LIMIT limit_val;
    $BODY$
    LANGUAGE sql;


CREATE OR REPLACE FUNCTION add_item(date INT, latitude NUMERIC, longitude NUMERIC) 
    RETURNS void AS
    $BODY$
    	INSERT INTO items(date, latitude, longitude) 
    	VALUES (date, latitude, longitude);
    $BODY$
    LANGUAGE sql;
