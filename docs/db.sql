CREATE TABLE items(
	id SERIAL PRIMARY KEY,
	date int NOT NULL,
	latitude NUMERIC NOT NULL,
	longitude NUMERIC NOT NULL	
)

CREATE OR REPLACE FUNCTION get_items(limit_num numeric=100) 
    RETURNS refcursor AS $$
    DECLARE
      	ref refcursor;
    BEGIN
	    OPEN ref FOR SELECT 
	        id,
	        date,
	        trim(to_char(latitude, '99D999999')),
	        trim(to_char(longitude, '99D999999'))
	    FROM items 
	    ORDER BY date DESC 
	    LIMIT limit_num;
	    RETURN ref;
    END;
    $$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION add_item(date INT, latitude NUMERIC, longitude NUMERIC) 
    RETURNS void AS $$
    BEGIN
    	INSERT INTO items(date, latitude, longitude) 
    	VALUES (date, latitude, longitude);
    END;
    $$ LANGUAGE plpgsql;

