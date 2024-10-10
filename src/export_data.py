import logging
from models import Session, WeatherData
from openpyxl import Workbook

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

EXPORT_FILE = "./src/data/weather_data.xlsx"


def export_to_excel():
    """
    Экспортирует последние 10 записей о погоде из базы данных в Excel файл.

    """

    session = Session()
    data = session.query(WeatherData).order_by(WeatherData.timestamp.desc()).limit(10).all()
    session.close()

    wb = Workbook()
    ws = wb.active
    ws.append([
        "Временная метка",
        "Температура (°C)",
        "Направление ветра",
        "Скорость ветра (м/с)",
        "Давление (мм рт. ст.)",
        "Тип осадков",
        "Количество осадков (мм)"
    ])

    for entry in reversed(data):
        ws.append([
            entry.timestamp,
            entry.temperature,
            entry.wind_direction,
            entry.wind_speed,
            entry.pressure,
            entry.precipitation_type,
            entry.precipitation_amount
        ])

    wb.save(EXPORT_FILE)
    logging.info("Данные успешно экспортированы в Excel")


if __name__ == "__main__":
    logging.info("Начало экспорта данных в Excel")
    export_to_excel()
    logging.info("Завершение экспорта данных в Excel")
