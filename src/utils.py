import json
import logging
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
rlt_file_path = os.path.join(current_dir, "../logs/utils.log")
abs_file_path = os.path.abspath(rlt_file_path)

logger = logging.getLogger("utils")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_transactions_from_excel(
    file_path=r"C:\Users\anisa\PycharmProjects\Course-Transaction-Analysis-\data\operations.xlsx",
) -> pd.DataFrame | Any:
    """Чтение Excel-файла и получение списка транзакций"""
    empty = pd.DataFrame()
    logger.info(f"Запрос на чтение Excel-файла {file_path}")
    try:
        transactions_df = pd.read_excel(file_path)
    except FileNotFoundError:
        logger.error("Ошибка! Файл не найден")
        print("Файл не найден. Пожалуйста, укажите другой путь для чтения файла")
        return empty
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")
        return empty
    else:
        logger.info("Запрос на преобразование данных DataFrame успешно выполнен")
        return transactions_df


def converting_data_to_json(data: Any) -> str:
    """Конвертация данных в JSON-строку"""
    logger.info("Запрос на форматирование данных в JSON-строку")
    if isinstance(data, pd.DataFrame):
        data = data.to_dict(orient="records")

    try:
        result = json.dumps(data, ensure_ascii=False, indent=4, default=str)
    except (TypeError, ValueError) as e:
        logger.error(f"Ошибка при конвертации в JSON: {e}")
        return json.dumps({"error": f"Ошибка при конвертации в JSON: {e}"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка при конвертации в JSON: {e}")
        return json.dumps({"error": f"Ошибка при конвертации в JSON: {e}"}, ensure_ascii=False)
    else:
        logger.info("Конвертация данных в формат JSON успешно завершена.")
        return result


def user_greeting(user_date: str) -> str | Any:
    """Приветствие в зависимости от времени суток"""
    try:
        dt = datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")
        hour = dt.hour
        if 5 <= hour < 12:
            return "Доброе утро!"
        elif 12 <= hour < 18:
            return "Добрый день!"
        elif 18 <= hour < 23:
            return "Добрый вечер!"
        else:
            return "Доброй ночи!"
    except Exception as e:
        logger.error(f"Ошибка в user_greeting: {e}")
        return "Здравствуйте!"
    finally:
        logger.info("Функция user_greeting выполнена успешно.")


def filter_operations(operations: pd.DataFrame, date: str) -> list[dict]:
    """Фильтрация операций с начала месяца до входящей даты"""
    logger.info("Запрос на фильтрацию банковских операций")
    try:

        def parse_mixed_dates(date_series):
            """Перебор форматов дат и приведение к единому формату"""
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d.%m.%Y %H:%M:%S", "%d.%m.%Y"):
                parsed_dates = pd.to_datetime(date_series, format=fmt, errors="coerce")
                if parsed_dates.notna().all():
                    return parsed_dates
            return pd.to_datetime(date_series, errors="coerce")

        operations["Дата операции"] = parse_mixed_dates(operations["Дата операции"])
        end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        start_date = end_date.replace(day=1)
        filtered = operations[(operations["Дата операции"] >= start_date) & (operations["Дата операции"] <= end_date)]
    except Exception as e:
        logger.error(f"Ошибка в filter_operations: {e}")
        return []
    else:
        logger.info("Фильтрация операций прошла успешно.")
        return filtered.to_dict(orient="records")


def get_list_cards(operations: list[dict]) -> list[dict]:
    """Возвращает список карт с номером, общей суммой и кешбэком"""
    logger.info("Запрос на получение данных по банковским картам")
    summary = {}
    for operation in operations:
        card = operation.get("Номер карты")
        if not card or str(card).strip() == "" or str(card) == "nan":
            continue
        last_digits = str(card)[-4:]
        amount = float(operation.get("Сумма операции", 0))
        if last_digits not in summary:
            summary[last_digits] = {"total_spent": 0}
        if amount > 0:
            summary[last_digits]["total_spent"] += amount

    cards = []
    for digits, data in summary.items():
        total = round(data["total_spent"], 2)
        cashback = round(total * 0.01, 2)
        cards.append({"last_digits": digits, "total_spent": total, "cashback": cashback})

    logger.info("Данные по банковским картам успешно сформированы.")
    return cards


def read_user_settings(
    file_path=r"C:\Users\anisa\PycharmProjects\Course-Transaction-Analysis-\user_settings.json",
) -> dict:
    """Получение пользовательских настроек для курса валют и котировок акций"""
    logger.info("Запрос на получение списка валют и акций для пользователя")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка при чтении настроек пользователя: {e}")
        return {"user_currencies": [], "user_stocks": []}


def currency_rate(api_key: str, currencies: list[str], date: str) -> list[dict]:
    """Получение курса валют к рублю через сервис Exchange Rates Data API"""
    logger.info("Запрос на получение курса заданных валют по отношению к рублю")
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        symbols = ",".join(currencies)
        url = f"https://api.apilayer.com/exchangerates_data/{formatted_date}?symbols={symbols}&base=RUB"

        payload = {}
        headers = {"apikey": api_key}

        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()

        rates = data.get("rates", {})
        result = []
        for currency in currencies:
            if currency in rates:
                rate = round(rates[currency], 2)
                result.append({"currency": currency, "rate": rate})
    except Exception as e:
        logger.error(f"Ошибка при получении курса валют: {e}")
        return []
    else:
        logger.info("Курсы валют получены.")
        return result


def stock_prices(api_key: str, stocks: list[str]) -> list[dict]:
    """Получение цен акций через сервис Finnhub"""
    logger.info("Запрос на получение цен для акций из списка")
    result = []
    for stock in stocks:
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={api_key}"
            response = requests.get(url)
            data = response.json()
            price = data.get("c")  # текущая цена
            if price:
                result.append({"stock": stock, "price": round(price, 2)})
            else:
                print(f"Цена для {stock} не найдена")
        except Exception as e:
            logger.error(f"Ошибка при получении котировки {stock}: {e}")
    logger.info("Котировки акций получены.")
    return result


def get_top_transactions(operations: list[dict]) -> list[dict]:
    """Получение топ-5 транзакций по сумме операций"""
    logger.info("Запрос на получение Топ-5 транзакций.")
    try:
        valid_ops = [
            op
            for op in operations
            if op.get("Номер карты") and str(op["Номер карты"]).strip() != "" or str(op["Номер карты"] != "nan")
        ]
        sorted_ops = sorted(valid_ops, key=lambda x: abs(float(x.get("Сумма операции", 0))), reverse=True)
        top_5 = sorted_ops[:5]
    except Exception as e:
        logger.error(f"Ошибка в get_top_transactions: {e}")
        return []
    else:
        logger.info("Топ-5 транзакций успешно сформирован.")
        return [
            {
                "date": op.get("Дата платежа"),
                "amount": round(op.get("Сумма операции", 0), 2),
                "category": op.get("Категория", ""),
                "description": op.get("Описание", ""),
            }
            for op in top_5
        ]
