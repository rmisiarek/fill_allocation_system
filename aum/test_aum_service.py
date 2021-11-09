import pytest


def test_aum_service_create_payload():
    from aum_service import AUMService

    t = AUMService(url="http://127.0.0.1:8001/assets_distribution/")
    payload = t.create_payload(accounts_number=3)

    percentage_sum = 0
    for elem in payload:
        percentage_sum += elem["percentage"]

    assert percentage_sum == 100
