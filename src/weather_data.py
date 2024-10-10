import asyncio
import logging
import requests
import numpy as np
from models import Session, WeatherData

API_URL = "https://api.open-meteo.com/v1/forecast"

# Значения координат взяты из Яндекс карт
LATITUDE = 55.698538  # Широта
LONGITUDE = 37.359576  # Долгота

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def wind_direction_to_text(degrees: float) -> np.ndarray:
    """
    Преобразует градусы ветра в текстовое представление направления.

    Весь круг (360 градусов) делится на 16 равных секторов, каждый из которых соответствует определенному направлению.
    Размер каждого сектора составляет 360 / 16 = 22.5 градусов.

    Args:
        degrees: Градусы ветра.

    Returns:
        directions[index]: Текстовое представление направления ветра.

    """

    directions = np.array(
        ["С", "ССВ", "СВ", "ВСВ", "В", "ВЮВ", "ЮВ", "ЮЮВ", "Ю", "ЮЮЗ", "ЮЗ", "ЗЮЗ", "З", "ЗСЗ", "СЗ", "ССЗ"]
    )
    index = round(degrees / 22.5) % 16
    return directions[index]


def hpa_to_mmhg(hpa: float) -> float:
    """
    Преобразует давление из гПа в мм рт. ст.

    Args:
        hpa: Давление в гПа.

    Returns:
        mmhg: Давление в мм рт. ст.

    """

    mmhg = hpa * 0.750062
    return mmhg


def determine_precipitation_type(precipitation_amount: float) -> str | None:
    """
    Определяет тип осадков в зависимости от количества осадков.

    Args:
        precipitation_amount: Количество осадков в мм.

    Returns:
        Тип осадков ('rain', 'unknown' или None).

    """

    if precipitation_amount == 0:
        return None

    elif precipitation_amount > 0:
        return 'rain'

    else:
        return 'unknown'


async def get_weather_data():
    """
    Получает данные о погоде через API и сохраняет их в базу данных.

    """

    params = {
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
        'current_weather': True,
        'hourly': 'temperature_2m,windspeed_10m,winddirection_10m,pressure_msl,precipitation'
    }
    try:
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            logging.info("Успешно получены данные о погоде")
            data = response.json()
        else:
            logging.error(f"Ошибка при получении данных о погоде. Код состояния:: {response.status_code}")
            raise SystemExit(1)

        current_weather = data['current_weather']
        hourly = data['hourly']

        wind_direction_text = wind_direction_to_text(current_weather['winddirection'])
        pressure_mmhg = hpa_to_mmhg(hourly['pressure_msl'][0])
        precipitation_type = determine_precipitation_type(hourly['precipitation'][0])

        weather_entry = WeatherData(
            temperature=current_weather['temperature'],
            wind_direction=wind_direction_text,
            wind_speed=current_weather['windspeed'],
            pressure=pressure_mmhg,
            precipitation_type=precipitation_type,
            precipitation_amount=hourly['precipitation'][0]
        )

        with Session.begin() as session:
            session.add(weather_entry)
            session.commit()

    except Exception as e:
        logging.error(f"Ошибка при обработке данных о погоде: {e}")


async def main():
    """
    Основная асинхронная функция, которая запускает процесс получения данных о погоде каждые 3 минуты.

    """

    while True:
        await get_weather_data()
        await asyncio.sleep(180)


if __name__ == "__main__":
    asyncio.run(main())
