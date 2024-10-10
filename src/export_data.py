from models import Session, WeatherData
from openpyxl import Workbook


def export_to_excel():
    session = Session()
    data = session.query(WeatherData).order_by(WeatherData.timestamp.desc()).limit(10).all()
    session.close()

    wb = Workbook()
    ws = wb.active
    ws.append(["Timestamp", "Temperature", "Wind Direction", "Wind Speed", "Pressure", "Precipitation Type",
               "Precipitation Amount"])

    for entry in reversed(data):
        ws.append([entry.timestamp, entry.temperature, entry.wind_direction, entry.wind_speed, entry.pressure,
                   entry.precipitation_type, entry.precipitation_amount])

    wb.save("./datas/weather_data.xlsx")


if __name__ == "__main__":
    export_to_excel()
