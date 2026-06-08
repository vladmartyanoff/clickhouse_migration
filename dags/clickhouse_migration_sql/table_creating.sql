
create table if not exists analytics.city_weather_data_ch (
	id UInt64,
	city_name String,
	temperature Float32,
	pressure Float32,
	humidity Float32,
	timestamp DateTime,
	updated_at DateTime default now()
)
Engine = ReplacingMergeTree(updated_at)
Primary Key (id)
ORDER BY id;
