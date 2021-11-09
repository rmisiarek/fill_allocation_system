from typing import Optional, List

from fastapi import FastAPI, status
from pydantic import BaseModel
import uvicorn
from fastapi_utils.tasks import repeat_every
import asyncio
import operator
from collections import OrderedDict
import requests


app = FastAPI()
lock = asyncio.Lock()

ACCOUNT_SPLIT = {}
POSITIONS_LIST = []

class TradeFillDTO(BaseModel):
    stock_ticker: str
    price: int
    quantity: int


class AssetsDistributionDTO(BaseModel):
    account_name: str
    percentage: int


class AssetsDistributionDTOList(BaseModel):
    data: List[AssetsDistributionDTO]



@app.on_event("startup")
@repeat_every(seconds=10)
async def send_positions_list() -> None:
    global POSITIONS_LIST
    if not POSITIONS_LIST:
        return

    async with lock:
        # TODO: change to asynchronous communication
        response = requests.post(
            url="http://position:8002/positions/", json={"data": POSITIONS_LIST}
        )
        POSITIONS_LIST = []


@app.post("/assets_distribution/", status_code=status.HTTP_200_OK)
async def assets_distribution(dto: AssetsDistributionDTOList):
    global ACCOUNT_SPLIT
    ACCOUNT_SPLIT = {}

    try:
        for data in dto.dict()["data"]:
            ACCOUNT_SPLIT.update({data["account_name"]: data["percentage"]})
    except KeyError:
        pass


@app.post("/trade_fill/", status_code=status.HTTP_200_OK)
async def trade_fill(dto: TradeFillDTO):
    global ACCOUNT_SPLIT

    trade_fill_quantity = dto.dict()["quantity"]
    trade_fill_ticker = dto.dict()["stock_ticker"]

    positions = calculate_quantity_for_accounts(
        account_split=ACCOUNT_SPLIT,
        trade_fill_quantity=trade_fill_quantity,
        trade_fill_ticker=trade_fill_ticker,
    )

    if positions:
        await add_to_positions_list(positions=positions)


def calculate_quantity_for_accounts(
    *, account_split, trade_fill_quantity, trade_fill_ticker
) -> dict:
    result = []
    account_quantity_dict = {}
    account_quantity_reminder_dict = {}

    if not account_split:
        return {}

    for account_name, percentage in account_split.items():
        quantity = (percentage * trade_fill_quantity) / 100
        account_quantity_dict.update({account_name: int(quantity)})
        decimal_reminder = quantity - int(quantity)
        account_quantity_reminder_dict.update({account_name: decimal_reminder})

    account_quantity_reminder_dict = OrderedDict(
        sorted(
            account_quantity_reminder_dict.items(),
            key=operator.itemgetter(1),
            reverse=True,
        )
    )

    index = 0
    while calculate_quantity_sum(account_quantity_dict) < trade_fill_quantity:
        account_at_index = list(account_quantity_reminder_dict.keys())[index]
        quantity = account_quantity_dict.get(account_at_index)
        account_quantity_dict.update({account_at_index: quantity + 1})
        index = index + 1

    for account_name, quantity in account_quantity_dict.items():
        result.append(
            {
                "account_name": account_name,
                "stock_ticker": trade_fill_ticker,
                "quantity": quantity,
            }
        )

    return {"positions": result}


def calculate_quantity_sum(account_quantity_dict):
    return sum(account_quantity_dict.values())
    

async def add_to_positions_list(*, positions):
    global POSITIONS_LIST
    async with lock:
        POSITIONS_LIST.append(positions)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
