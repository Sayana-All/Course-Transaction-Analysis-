import pytest
from unittest.mock import patch
from src.views import main_page


@patch("src.views.load_dotenv")
@patch("src.views.stock_prices")
@patch("src.views.currency_rate")
@patch("src.views.get_top_transactions")
@patch("src.views.get_list_cards")
@patch("src.views.user_greeting")
@patch("src.views.read_user_settings")
@patch("src.views.filter_operations")
@patch("src.views.get_transactions_from_excel")
def test_main_page_success(
    mock_get_transactions,
    mock_filter_operations,
    mock_read_user_settings,
    mock_user_greeting,
    mock_get_list_cards,
    mock_get_top_transactions,
    mock_currency_rate,
    mock_stock_prices,
    mock_load_dotenv,
    mock_transactions,
    mock_cards,
    mock_top_transactions,
    mock_currency_rates,
    mock_stock_prices_fixture,
    mock_settings,
):
    """Тестирование успешного формирования Главной страницы с использованием тестовых фикстур"""
    mock_get_transactions.return_value = "mock_df"
    mock_filter_operations.return_value = mock_transactions
    mock_read_user_settings.return_value = mock_settings
    mock_user_greeting.return_value = "Добрый день!"
    mock_get_list_cards.return_value = mock_cards
    mock_get_top_transactions.return_value = mock_top_transactions
    mock_currency_rate.return_value = mock_currency_rates
    mock_stock_prices.return_value = mock_stock_prices_fixture

    result = main_page("2024-05-25 12:00:00")

    assert "greeting" in result
    assert result["greeting"] == "Добрый день!"
    assert result["cards"] == mock_cards
    assert result["top_transactions"] == mock_top_transactions
    assert result["currency_rates"] == mock_currency_rates
    assert result["stock_prices"] == mock_stock_prices_fixture


@patch("src.views.get_transactions_from_excel", side_effect=Exception("Ошибка чтения Excel"))
@patch("src.views.load_dotenv")
def test_main_page_error(mock_load_dotenv, mock_get_transactions):
    result = main_page("2024-05-25 12:00:00")
    assert "error" in result
    assert result["error"] == "Ошибка чтения Excel"
