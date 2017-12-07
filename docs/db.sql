CREATE TABLE pq.items(
	id SERIAL PRIMARY KEY,
	latitude NUMERIC NOT NULL,
	longitude NUMERIC NOT NULL,
	date int NOT NULL
)