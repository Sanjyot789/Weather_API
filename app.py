import requests
import pandas as pd
from sqlalchemy import create_engine, text
# from typing import JsonType


if __name__ == '__main__':
    print("This is an api you cannot use it explictly")
    exit()


class DataAPI:
    def __init__(self, api_key : str, database_url : str) -> None:
        self.api_key = api_key
        self.database_url = database_url
        self.engine = create_engine(database_url)
        
    def fetch_data(self, city_name : str) :
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}'
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"API request failed for {city_name}")
        
        data = response.json()
        #print(data)
        return data

    def transform_data(self, data ) -> pd.core.frame.DataFrame:
        city = data.get('name')
        temperature = round(data.get('main', {}).get('temp') - 273.15,2 )
        humidity = data.get('main', {}).get('humidity')
        wind_speed = data.get('wind', {}).get('speed')
        dt_timestamp = data.get('dt')
        dt_datetime = pd.to_datetime(dt_timestamp, unit='s', utc=True)

        df = pd.DataFrame({
            'city': [city],
            'dt': [dt_datetime],
            'temperature': [temperature],
            'humidity': [humidity],
            'wind_speed': [wind_speed]
        })
        #print(df)
        return df

    def upsert_data(self, df, table_name): 
        data_record = df.to_dict(orient='records')[0]
        # print(type(data_record))
        # print(f'{data_record=}')
        with self.engine.connect() as conn:   # do not used pd.to_sql because of on conflict issue
            create_sql_statement = text(f''' 
                CREATE TABLE IF NOT EXISTS weather (
                city TEXT NOT NULL,
                dt TIMESTAMP WITH TIME ZONE NOT NULL,
                temperature NUMERIC,
                humidity NUMERIC,
                wind_speed NUMERIC,
                PRIMARY KEY (city, dt));
            ''')
            conn.execute(create_sql_statement)

            sql_statement = text(f'''
                INSERT INTO {table_name} (city, dt, temperature, humidity, wind_speed)
                VALUES ('{data_record['city']}', '{data_record['dt']}', '{data_record['temperature']}', '{data_record['humidity']}', '{data_record['wind_speed']}')
                ON CONFLICT (city, dt) DO NOTHING;
            ''')
            conn.execute(sql_statement)  # Pass the record as a single parameter, not keyword arguments
            conn.commit()
    def get_data(self, table_name):
        df = pd.read_sql_table(table_name, self.engine)
        return df

# Example Usage:
# api = DataAPI(api_key='api key', database_url='postgresql://postgres:1234@localhost:5432/weather_db')
# city_name = 'Mumbai, IN'
# data = api.fetch_data(city_name)
# df = api.transform_data(data)
# api.upsert_data(df, table_name='weather')
# df = api.get_data(table_name='weather')
# print(df)



# CREATE DATABASE IF NOT EXISTS weather_db;
