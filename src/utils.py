import json
import logging
import os
from typing import Any, Hashable

import pandas as pd
from pandas import DataFrame

current_dir = os.path.dirname(os.path.abspath(__file__))
rlt_file_path = os.path.join(current_dir, "../logs/utils.log")
abs_file_path = os.path.abspath(rlt_file_path)

logger = logging.getLogger("utils")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_transactions_from_excel(file_path: str) -> DataFrame:
    """Чтение Excel-файла и получение списка транзакций"""
    logger.info(f"Запрос на чтение Excel-файла {file_path}")
    try:
        transactions_df = pd.read_excel(file_path)
        return transactions_df
    except FileNotFoundError:
        logger.error("Ошибка! Файл не найден")
        print("Файл не найден. Пожалуйста, укажите другой путь для чтения файла")
        return []
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")
        return []


def converting_data_to_json(data: DataFrame) -> list[dict[Hashable, Any]] | str:
    """Преобразует данные в JSON-формат для веб-страниц"""
    logger.info("Запрос на преобразование данных из DataFrame в JSON-формат")
    try:
        new_data = data.to_dict(orient="records")
    except TypeError:
        logger.error("Ошибка! Неверный формат данных")
        print("Неверный формат данных. Невозможно преобразовать.")
        return []
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")
        return []
    else:
        if len(new_data) > 0:
            try:
                data_json = json.dumps(new_data)
            except ValueError:
                logger.error("Invalid JSON data.")
                return []
            except Exception as e:
                logger.error(f"Произошла ошибка {e}")
                return []
            else:
                logger.info("Словарь транзакций успешно создан.")
                return data_json
        else:
            print("Словарь операций пустой")
            return []


def user_greeting(user_date: str) -> str:
    """Приветствие пользователя в зависимости от времени суток"""
    pass


def filter_operations(operations: DataFrame, date: str) -> list[dict]:
    """Фильтрация операций по заданной дате. Выводит операции за последние 3 месяца"""
    pass


def get_list_cards(operations: list[dict]) -> list[dict]:
    """Функция отображения информации по банковским картам пользователя"""
    pass


def get_top_transactions(operations: list[dict]) -> list[dict]:
    """Получение топ-5 транзакций по сумме операций"""
    pass


def currency_rate(api_key: str, currency: list) -> list[dict]:
    """Отображение курса валют, указанных в списке"""
    pass


def stock_prices(api: str, stock: dict) -> list[dict]:
    """Котировка выбранных акций"""
    pass


if __name__ == "__main__":
    result = get_transactions_from_excel(
        r"C:\Users\PC\PycharmProjects\Course-Transaction-Analysis-\data\operations.xlsx"
    )
    print(result.shape)
    print(type(result))

