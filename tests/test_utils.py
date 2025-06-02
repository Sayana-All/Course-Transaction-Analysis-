import json
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest
from pandas import Timestamp

from src.utils import (converting_data_to_json, currency_rate, filter_operations, get_list_cards, get_top_transactions,
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


@pytest.mark.parametrize(
    "input_date,expected",
    [
        ("2021-10-20 06:00:00", "Доброе утро!"),
        ("2021-10-20 13:00:00", "Добрый день!"),
        ("2021-10-20 19:00:00", "Добрый вечер!"),
        ("2021-10-20 02:00:00", "Доброй ночи!"),
        ("some_date", "Здравствуйте!"),
    ],
)
def test_user_greeting(input_date: str, expected: str):
    """Тестирование функции приветствия пользователя в зависимости от времени суток"""
    assert user_greeting(input_date) == expected


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


@pytest.mark.parametrize(
    "input_data,expected",
    [
        ({"key": "value"}, '{"key": "value"}'),
        ([{"name": "Alice"}, {"name": "Bob"}], '[{"name": "Alice"}, {"name": "Bob"}]'),
        (pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}]), '[{"a": 1, "b": 2}, {"a": 3, "b": 4}]'),
        ("строка", '"строка"'),
        (123, "123"),
    ],
)
def test_converting_data_to_json(input_data, expected):
    """Тестирование функции конвертации данных в JSON-строку и обратное преобразование"""
    result = converting_data_to_json(input_data)
    assert json.loads(result) == json.loads(expected)


def test_crashed_converting_data_to_json_with_func():
    """Обработка исключения при конвертации с использованием объекта функции"""

    def sample_func():
        return "Some data"

    result = converting_data_to_json(sample_func)
    assert isinstance(result, str)
    assert result.startswith('"<function test_crashed_converting_data_to_json_with_func.<locals>.sample_func')
