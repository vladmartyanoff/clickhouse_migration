create table if not exists amplitude_weather (
	id serial primary key,
	city_name varchar(50),
	temperature float,
	pressure float,
	humidity float,
	timestamp timestamp,
	created_at date default now()
)
