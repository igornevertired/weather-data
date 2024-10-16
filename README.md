# Проект: Мониторинг погоды в Сколтехе

Этот проект представляет собой 2 Python скрипта, один из которых автоматически запрашивает данные погоды в районе Сколтеха через API и сохраняет их в базу данных. Второй скрипт экспортирует данные из базы данных в Excel файл.

## Основные функции

### Запрос данных погоды и их сохранение в базу данных:
- Скрипт автоматически запрашивает данные погоды каждые 3 минуты через API.
- Полученные данные включают: температуру, направление и скорость ветра, давление воздуха, тип и количество осадков.
- Данные сохраняются в базу данных PostgreSQL.

### Экспорт данных из базы в Excel:
- Скрипт поддерживает команду из консоли для экспорта данных из базы данных в файл формата `.xlsx`.
- Экспорт не прерывает процесс запроса данных о погоде.
- Файл `.xlsx` содержит все запрашиваемые поля и 10 последних полученных данных.

### Структура проекта
# src
 - weather_data.py: Основной скрипт, который запрашивает данные погоды и сохраняет их в базу данных.
 - models.py: Определение моделей данных с использованием SQLAlchemy.
 - export_data.py: Скрипт для экспорта данных из базы данных в Excel файл.
   ## data
   - weather_data.xlsx - Пример файла Excel с выгруженными данными.
   ## configs
   - db_config.yaml - YAML файл с конфигурацией подключения к базе данных PostgreSQL

