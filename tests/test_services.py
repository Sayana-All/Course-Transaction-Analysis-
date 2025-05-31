import json

import pytest

from src.services import calculate_increased_cashback, search_phone_numbers, simple_search


def test_calculate_increased_cashback(mock_extended_transactions):
    """Тестирование функции анализа категорий повышенного кешбэка"""
    result = calculate_increased_cashback(mock_extended_transactions, "2024", "05")
    data = json.loads(result)
    assert isinstance(data, dict)
    assert data["Еда"] == 10
    assert data["Развлечения"] == 3


def test_simple_search_by_category(mock_extended_transactions):
    """Тестирование функции поиска транзакции по выбранной категории"""
    result = simple_search(mock_extended_transactions, "еда")
    data = json.loads(result)

    assert len(data) == 2
    assert data[0]["Категория"].lower() == "еда"


def test_simple_search_by_description(mock_extended_transactions):
    """Тестирование функции поиска транзакций по описанию"""
    result = simple_search(mock_extended_transactions, "супермаркет")
    data = json.loads(result)

    assert len(data) == 1
    assert "супермаркет" in data[0]["Описание"]


def test_search_phone_numbers(mock_extended_transactions):
    """Тестирование функции поиска транзакций по номеру телефона в описании"""
    result = search_phone_numbers(mock_extended_transactions)
    data = json.loads(result)

    assert isinstance(data, list)
    assert len(data) == 1
    assert "+7 (912) 345-67-89" in data[0]["Описание"]
