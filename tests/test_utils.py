from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest
from pandas import Timestamp

from src.utils import (currency_rate, filter_operations, get_list_cards, get_top_transactions,
                       get_transactions_from_excel, read_user_settings, stock_prices, user_greeting)


def test_get_transactions_from_excel(sample_excel_file):
    df = get_transactions_from_excel(sample_excel_file)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert set(["Номер карты", "Сумма операции", "Категория", "Описание", "Дата операции"]).issubset(df.columns)


def test_get_transactions_file_not_found():
    result = get_transactions_from_excel("non_existent_file.xlsx")
    assert isinstance(result, pd.DataFrame)
    assert result.empty


def test_user_greeting():
    """Тестирование функции приветствия пользователя в зависимости от времени суток"""
    assert user_greeting("2024-01-21 08:00:00") == "Доброе утро!"
    assert user_greeting("2024-02-22 13:00:00") == "Добрый день!"
    assert user_greeting("2024-03-23 20:00:00") == "Добрый вечер!"
    assert user_greeting("2024-04-24 01:00:00") == "Доброй ночи!"
    assert user_greeting("some_date") == "Здравствуйте!"


def test_filter_operations(mock_transactions):
    """Тестирование функции фильтрации операции по указанной дате и времени"""
    df = pd.DataFrame(mock_transactions)
    result = filter_operations(df, "2024-05-25 23:59:59")
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == {
        "Дата операции": Timestamp("2024-05-25 09:00:00"),
        "Категория": "Еда",
        "Номер карты": "****1234",
        "Описание": "Покупка в магазине",
        "Сумма операции": 1000,
    }


def test_get_list_cards(mock_transactions):
    """Тестирование функции по отображению списка карт и информации по ним"""
    result = get_list_cards(mock_transactions)
    assert isinstance(result, list)
    assert result[0]["last_digits"] == "1234"
    assert result[1]["total_spent"] == 500.0
    assert result[0]["cashback"] == 10.0


def test_get_top_transactions(mock_transactions):
    """Тестирование функции получения топ-5 транзакций из списка"""
    result = get_top_transactions(mock_transactions)
    assert isinstance(result, list)
    assert len(result) <= 5
    assert result[0]["amount"] == 1000


@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD"], "user_stocks": ["AAPL"]}')
def test_read_user_settings(mock_file):
    """Тестирование функции по чтению пользовательских настроек по курсам валют и акциям из файла"""
    result = read_user_settings("dummy_path.json")
    assert result["user_currencies"] == ["USD"]
    assert result["user_stocks"] == ["AAPL"]


@patch("requests.request")
def test_currency_rate(mock_request, mock_settings):
    """Тестирование функции по получению курса валют"""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"rates": {"USD": 0.013}}
    mock_request.return_value = mock_response

    result = currency_rate("fake_key", ["USD"], "2024-05-25 12:00:00")
    assert result == [{"currency": "USD", "rate": 0.01}]


@patch("requests.get")
def test_stock_prices(mock_get, mock_settings):
    """Тестирование функции по получению котировок акций"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"c": 123.456}
    mock_get.return_value = mock_response

    result = stock_prices("fake_key", ["AAPL"])
    assert result == [{"stock": "AAPL", "price": 123.46}]
