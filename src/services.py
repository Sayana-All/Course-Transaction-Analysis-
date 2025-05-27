import logging
import os
import re
from collections import defaultdict
from datetime import datetime
from typing import Any

current_dir = os.path.dirname(os.path.abspath(__file__))
rlt_file_path = os.path.join(current_dir, "../logs/services.log")
abs_file_path = os.path.abspath(rlt_file_path)

logger = logging.getLogger("services")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def calculate_increased_cashback(operations: list[dict[str, Any]], year: str, month: str) -> dict[str, float]:
    """Анализ категорий для подсчета повышенного кэшбэка"""
    logger.info(f"Анализ повышенного кэшбэка за {year}-{month}")
    result = defaultdict(float)

    for op in operations:
        date_raw = op.get("Дата операции")
        amount_raw = op.get("Сумма операции")
        category = op.get("Категория")

        if not date_raw or not amount_raw or not category:
            continue

        try:
            if isinstance(date_raw, str):
                try:
                    date = datetime.strptime(date_raw, "%Y-%m-%d")
                except ValueError:
                    try:
                        date = datetime.strptime(date_raw, "%d.%m.%Y %H:%M:%S")
                    except ValueError:
                        date = datetime.strptime(date_raw, "%d.%m.%Y")
            elif isinstance(date_raw, datetime):
                date = date_raw
            else:
                continue

            if str(date.year) == year and f"{date.month:02}" == month:
                amount = float(amount_raw)
                if amount > 0:
                    cashback = amount * 0.01
                    result[category] += round(cashback)
        except Exception as e:
            logger.warning(f"Ошибка при обработке записи: {e}")
            continue

    logger.info("Завершен расчет кэшбэка по категориям.")
    return dict(result)


def simple_search(operations: list[dict], query: str) -> list[dict]:
    """
    Возвращает список транзакций, содержащих строку `query` в категории или описании.
    """
    logger.info(f"Поиск по строке: '{query}'")
    query_lower = query.lower()

    result = list(
        filter(
            lambda op: query_lower in str(op.get("Категория", "")).lower()
            or query_lower in str(op.get("Описание", "")).lower(),
            operations,
        )
    )

    logger.info(f"Найдено {len(result)} совпадений")
    return result


def search_phone_numbers(operations: list[dict]) -> list[dict]:
    """Поиск операций по номеру телефона в описании"""
    phone_pattern = re.compile(r"\+7\s?\(?9\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}")

    result = list(filter(lambda op: bool(phone_pattern.search(str(op.get("Описание", "")))), operations))

    logger.info(f"Найдено {len(result)} транзакций с номерами телефонов")
    return result
