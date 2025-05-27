import functools
import logging
import os
from datetime import datetime, timedelta
from typing import Callable, Literal, Optional

import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
rlt_file_path = os.path.join(current_dir, "../logs/reports.log")
abs_file_path = os.path.abspath(rlt_file_path)

logger = logging.getLogger("reports")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def save_file(filename: Optional[str] = None, file_format: Literal["excel", "csv"] = "excel"):
    """Функция-декоратор для сохранения файлов в формате excel или csv"""

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if not isinstance(result, pd.DataFrame):
                logger.warning("Невозможно сохранить, так как результат функции не DataFrame.")
                return result

            ext = "xlsx" if file_format == "excel" else "csv"
            file_name = filename or f"{func.__name__}_{datetime.now().strftime('%d-%m-%Y')}.{ext}"

            project_root = os.path.abspath(os.path.join(current_dir, ".."))
            reports_dir = os.path.join(project_root, "data", "reports")
            os.makedirs(reports_dir, exist_ok=True)
            full_path = os.path.join(reports_dir, file_name)

            try:
                if file_format == "excel":
                    result.to_excel(full_path, index=False)
                elif file_format == "csv":
                    result.to_csv(full_path, index=False, encoding="utf-8")
                else:
                    raise ValueError("Неподдерживаемый формат файла.")
                logger.info(f"Результат сохранён в файл {full_path}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении файла: {e}")
            return result

        return wrapper

    return decorator


@save_file(file_format="csv")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает отчет по тратам за последние 3 месяца с указанной даты по заданной категории"""
    if date is None:
        now = datetime.now()
    else:
        try:
            now = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            logger.error("Дата должна быть в формате YYYY-MM-DD.")
            return pd.DataFrame()

    three_months_ago = now - timedelta(days=90)
    transactions = transactions.copy()
    try:

        def parse_mixed_dates(date_series):
            """Перебор форматов дат и приведение к единому формату"""
            for fmt in ("%d.%m.%Y %H:%M:%S", "%d.%m.%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                parsed = pd.to_datetime(date_series, format=fmt, errors="coerce")
                if parsed.notna().sum() > 0:
                    return parsed
            return pd.to_datetime(date_series, errors="coerce")

        transactions["Дата операции"] = parse_mixed_dates(transactions["Дата операции"])
    except Exception as e:
        logger.error(f"Ошибка преобразования дат: {e}")
        return pd.DataFrame()

    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= now)
    ]

    return filtered_transactions
