# Weather_API
 
## Overview

This Python-based data pipeline allows you to fetch, transform, and store real-time weather data for various cities using the OpenWeatherMap API. It simplifies the process of integrating weather information into your projects and applications.


1. **Clone the Repository:**

   ```shell
   git clone https://github.com/Sanjyot789/Weather_API.git

2. **Install Required Packages:**

Make sure you have Python 3.11 installed. You can install the required packages using pip:
```
pip install requests pandas sqlalchemy psycopg2
```

3. **Configure the Database:**

Before using the pipeline, ensure you have a PostgreSQL database available. Update the database_url in the code to point to your database.

3. **Initialization:**

Initialize the DataAPI class by providing your OpenWeatherMap API key and database URL.
```
api = DataAPI(api_key='YOUR_API_KEY', database_url='YOUR_DATABASE_URL')
```

3. **Code Explanation:**

DataAPI class: Manages the OpenWeatherMap API interaction and database operations.
fetch_data: Retrieves weather data for a specified city.
transform_data: Transforms the raw data into a structured DataFrame.
upsert_data: Stores data in the PostgreSQL database with conflict handling.
get_data: Retrieves stored data from the database.
