import pytest

from src.services import calculate_increased_cashback, search_phone_numbers, simple_search


def test_calculate_increased_cashback(mock_extended_transactions):
    """Тестирование функции анализа категорий повышенного кешбэка"""
    result = calculate_increased_cashback(mock_extended_transactions, "2024", "05")
    assert isinstance(result, dict)
    assert result["Еда"] == 10
    assert result["Развлечения"] == 3


def test_simple_search_by_category(mock_extended_transactions):
    """Тестирование функции поиска транзакции по выбранной категории"""
    result = simple_search(mock_extended_transactions, "еда")
    assert len(result) == 2
    assert result[0]["Категория"].lower() == "еда"


def test_simple_search_by_description(mock_extended_transactions):
    """Тестирование функции поиска транзакций по описанию"""
    result = simple_search(mock_extended_transactions, "супермаркет")
    assert len(result) == 1
    assert "супермаркет" in result[0]["Описание"]


def test_search_phone_numbers(mock_extended_transactions):
    """Тестирование функции поиска транзакций по номеру телефона в описании"""
    result = search_phone_numbers(mock_extended_transactions)
    assert isinstance(result, list)
    assert len(result) == 1
    assert "+7 (912) 345-67-89" in result[0]["Описание"]
