import pytest
import pandas as pd

@pytest.fixture
def mock_transactions():
    return [
        {"Дата операции": "2024-05-25 09:00:00", "Номер карты": "****1234", "Сумма операции": 1000, "Категория": "Еда", "Описание": "Покупка в магазине"},
        {"Дата операции": "2024-05-10 20:00:00", "Номер карты": "****5678", "Сумма операции": 500, "Категория": "Транспорт", "Описание": "Метро"},
    ]


@pytest.fixture
def mock_cards():
    return [{"last_digits": "1234", "total_spent": 1000, "cashback": 10}]


@pytest.fixture
def mock_top_transactions():
    return [{"amount": 1000, "category": "Еда", "description": "Покупка в магазине", "date": "2024-05-24"}]


@pytest.fixture
def mock_currency_rates():
    return [{"currency": "USD", "rate": 0.01}]


@pytest.fixture
def mock_stock_prices_fixture():
    return [{"stock": "AAPL", "price": 123.45}]


@pytest.fixture
def mock_settings():
    return {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}


@pytest.fixture
def mock_extended_transactions():
    return [
        {
            "Номер карты": "****1234",
            "Сумма операции": 1000,
            "Категория": "Еда",
            "Описание": "Покупка продуктов в супермаркете",
            "Дата операции": "2024-05-15",
        },
        {
            "Номер карты": "****1234",
            "Сумма операции": 300,
            "Категория": "Развлечения",
            "Описание": "Билет в кино +7 (912) 345-67-89",
            "Дата операции": "2024-05-08",
        },
        {
            "Номер карты": "****5678",
            "Сумма операции": 700,
            "Категория": "Еда",
            "Описание": "Заказ еды через доставку",
            "Дата операции": "2024-03-10",
        },
    ]


@pytest.fixture
def mock_transaction_df(mock_extended_transactions):
    return pd.DataFrame(mock_extended_transactions)
