import pytest
from fastapi.testclient import TestClient
from service import app

client = TestClient(app)


def test_calculate_quantity_for_accounts():
    from service import calculate_quantity_for_accounts

    result = calculate_quantity_for_accounts(
        account_split={}, trade_fill_quantity=12, trade_fill_ticker="AXA"
    )
    assert result == {}

    result = calculate_quantity_for_accounts(
        account_split={"Account_1": 15, "Account_2": 43, "Account_3": 42},
        trade_fill_quantity=131,
        trade_fill_ticker="AXA",
    )

    expected_result = {
        "positions": [
            {"account_name": "Account_1", "stock_ticker": "AXA", "quantity": 20},
            {"account_name": "Account_2", "stock_ticker": "AXA", "quantity": 56},
            {"account_name": "Account_3", "stock_ticker": "AXA", "quantity": 55},
        ]
    }

    assert result == expected_result


def test_receive_trade_fill():
    response = client.post(
        "/trade_fill/",
        json={"stock_ticker": "SAP", "price": 21, "quantity": 88},
    )
    assert response.status_code == 200
