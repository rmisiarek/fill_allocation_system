from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class AccountData(BaseModel):
    account_name: str
    stock_ticker: str
    quantity: int


class PositionDTOList(BaseModel):
    positions: List[AccountData]


class PositionsBatchDTO(BaseModel):
    data: List[PositionDTOList]


@app.post("/positions/")
async def positions(dto: PositionsBatchDTO):
    for position_list in dto.dict()["data"]:
        for elem in position_list["positions"]:
            print(f"{elem['account_name']}: {elem['quantity']} {elem['stock_ticker']}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
