import json
import os
from glob import glob

import pandas as pd
import pytest

from src.reports import save_file, spending_by_category


def test_spending_by_category_valid_input(mock_transaction_df):
    """Проверка валидного ввода — корректная категория и дата"""
    result = spending_by_category(mock_transaction_df, category="Еда", date="2024-05-25")
    data = json.loads(result)

    assert isinstance(data, list)
    assert all(row["Категория"] == "Еда" for row in data)
    assert all(pd.to_datetime(row["Дата операции"]) <= pd.to_datetime("2024-05-25") for row in data)
    assert len(data) == 2


def test_spending_by_category_invalid_date(mock_transaction_df):
    """Тестирование функции на невалидную дату"""
    result = spending_by_category(mock_transaction_df, category="Еда", date="invalid-date")
    data = json.loads(result)
    assert isinstance(data, list)
    assert data == []


def test_spending_by_category_no_matching_category(mock_transaction_df):
    """Тестирование функции с проверкой на ненайденную категорию"""
    result = spending_by_category(mock_transaction_df, category="Несуществующая", date="2024-05-25")
    data = json.loads(result)
    assert isinstance(data, list)
    assert data == []


def test_spending_by_category_out_of_range_date(mock_transaction_df):
    """Проверка работы функции с датой вне диапазона получения данных"""
    result = spending_by_category(mock_transaction_df, category="Развлечения", date="2023-01-01")
    data = json.loads(result)
    assert isinstance(data, list)
    assert data == []


@save_file(file_format="excel")
def dummy_excel_report_func():
    return pd.DataFrame({"Категория": ["Транспорт", "Жильё"], "Сумма": [300, 15000]})


def test_save_file_creates_excel_file_in_reports_dir():
    """Проверка, что декоратор сохраняет Excel-файл в data/reports и возвращает DataFrame"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    reports_dir = os.path.join(project_root, "data", "reports")
    os.makedirs(reports_dir, exist_ok=True)

    for f in glob(os.path.join(reports_dir, "dummy_excel_report_func_*.xlsx")):
        os.remove(f)

    result = dummy_excel_report_func()

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2, 2)

    matching_files = glob(os.path.join(reports_dir, "dummy_excel_report_func_*.xlsx"))
    assert len(matching_files) == 1

    saved_file = matching_files[0]
    df_loaded = pd.read_excel(saved_file)
    assert df_loaded.equals(result)

    os.remove(saved_file)
