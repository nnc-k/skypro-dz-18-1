import csv
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем настройки подключения
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def load_data_from_csv(file_name: str, skip_header: bool = False) -> list:
    """Читает CSV-файл и возвращает список строк."""
    # Ищем папку north_data в корне проекта
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "north_data" / file_name

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)

        # Если в файле есть заголовки, пропускаем первую строку
        if skip_header:
            return data[1:]
        return data


def main() -> None:
    # 1. Подключаемся к базе данных
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        conn.autocommit = True
        cursor = conn.cursor()
        print("Подключение к БД успешно!")
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return

    # 2. Заполняем таблицу employees (пропускаем заголовок)
    print("Загружаем сотрудников...")
    employees_data = load_data_from_csv("employees_data.csv", skip_header=True)
    for row in employees_data:
        cursor.execute(
            "INSERT INTO employees (first_name, last_name, title, birth_date, notes) VALUES (%s, %s, %s, %s, %s)",
            (row[0], row[1], row[2], row[3], row[4]),
        )

    # 3. Заполняем таблицу customers (пропускаем заголовок)
    print("Загружаем клиентов...")
    customers_data = load_data_from_csv("customers_data.csv", skip_header=True)
    for row in customers_data:
        cursor.execute(
            "INSERT INTO customers (customer_id, company_name, contact_name) VALUES (%s, %s, %s)",
            (row[0], row[1], row[2]),
        )

    # 4. Заполняем таблицу orders (заголовка нет, начинаем сразу с данных)
    print("Загружаем заказы...")
    orders_data = load_data_from_csv("orders_data.csv", skip_header=True)
    for row in orders_data:
        cursor.execute(
            "INSERT INTO orders (order_id, customer_id, employee_id, order_date, ship_city) VALUES (%s, %s, %s, %s, %s)",
            (row[0], row[1], row[2], row[3], row[4]),
        )

    # Закрываем соединение
    cursor.close()
    conn.close()
    print("Все данные успешно загружены в базу данных!")


if __name__ == "__main__":
    main()
