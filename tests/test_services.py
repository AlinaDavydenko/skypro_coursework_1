import json

import pytest

from src.services import get_transactions_fizlicam


@pytest.fixture
def sample_dict_transaction():
    return [
        {"Описание": "Константин Л."},
        {"Описание": "Оплата услуг"},
    ]


def test_get_transactions_fizlicam_success(sample_dict_transaction):
    result = get_transactions_fizlicam(sample_dict_transaction)
    expected = json.dumps([], ensure_ascii=False)
    assert result == expected


def test_get_transactions_fizlicam_no_match(sample_dict_transaction):
    """Проверка если в списке нет данных соответствующих паттерну, выводим пустой список"""
    pattern = r""
    result = get_transactions_fizlicam(sample_dict_transaction)
    expected = json.dumps([])
    assert result == expected


def test_get_transactions_fizlicam_empty_input():
    """Проверка, паттерн корректный но нет данных"""
    pattern = r"Константин Л."
    expected_result = "[]"

    result = get_transactions_fizlicam([])
    assert result == expected_result
