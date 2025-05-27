import pandas as pd
import pytest
from src.reports import spending_by_category


def test_spending_by_category_valid_input(mock_transaction_df):
    """Тестирование функции по валидации данных по тратам в заданной категории"""
    result = spending_by_category(mock_transaction_df, category="Еда", date="2024-05-25")
    assert isinstance(result, pd.DataFrame)
    assert (result["Категория"] == "Еда").all()
    assert (result["Дата операции"] <= pd.to_datetime("2024-05-25")).all()
    assert result.shape[0] == 2  # Одна запись "Еда" в пределах 3 месяцев


def test_spending_by_category_invalid_date(mock_transaction_df):
    """Проверка исключения из-за указания нечитаемой даты"""
    result = spending_by_category(mock_transaction_df, category="Еда", date="invalid-date")
    assert isinstance(result, pd.DataFrame)
    assert result.empty


def test_spending_by_category_no_matching_category(mock_transaction_df):
    """Проверка исключения из-за указания категории, не выявленной в списке транзакций"""
    result = spending_by_category(mock_transaction_df, category="Непонятная_Категория", date="2024-05-25")
    assert isinstance(result, pd.DataFrame)
    assert result.empty


def test_spending_by_category_out_of_range_date(mock_transaction_df):
    """Проверка исключения из-за указания слишком ранней даты"""
    result = spending_by_category(mock_transaction_df, category="Развлечения", date="2023-05-25")
    assert isinstance(result, pd.DataFrame)
    assert result.empty