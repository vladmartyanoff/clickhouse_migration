 INSERT INTO analytics.city_weather_data_ch (id, city_name, temperature, pressure, humidity, timestamp, updated_at)
        SELECT id, city_name, temperature, pressure, humidity, timestamp, now() as updated_at
        FROM postgresql('185.12.95.120:5432', 'airflow', 'city_weather_data', 'v_airflow_admin', '18191617')
        WHERE updated_at > (SELECT coalesce(max(updated_at), toDateTime('1970-01-01 00:00:00')) FROM analytics.city_weather_data_ch)

  
		

