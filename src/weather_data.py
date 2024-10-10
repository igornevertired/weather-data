import asyncio
import requests
from models import Session, WeatherData

API_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 55.6761
LONGITUDE = 37.4778


async def fetch_weather_data():
    params = {
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
        'current_weather': True,
        'hourly': 'temperature_2m,windspeed_10m,winddirection_10m,pressure_msl,precipitation'
    }
    response = requests.get(API_URL, params=params)
    print(response)
    data = response.json()

    current_weather = data['current_weather']
    hourly = data['hourly']

    weather_entry = WeatherData(
        temperature=current_weather['temperature'],
        wind_direction=current_weather['winddirection'],
        wind_speed=current_weather['windspeed'],
        pressure=hourly['pressure_msl'][0],
        precipitation_type='rain',  # Assuming rain for simplicity
        precipitation_amount=hourly['precipitation'][0]
    )

    session = Session()
    session.add(weather_entry)
    session.commit()
    session.close()


async def main():
    while True:
        print('here')
        await fetch_weather_data()
        await asyncio.sleep(180)  # Wait for 3 minutes


if __name__ == "__main__":
    asyncio.run(main())
