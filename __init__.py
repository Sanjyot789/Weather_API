from app import *


api = DataAPI(api_key='your api key', database_url='postgresql://postgres:1234@localhost:5432/weather_db')
city_name = 'Mumbai, IN'
data = api.fetch_data(city_name)
df = api.transform_data(data)
api.upsert_data(df, table_name='weather')
df = api.get_data(table_name='weather')
print(df)