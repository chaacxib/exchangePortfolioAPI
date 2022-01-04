import json
# from mangum import Mangum
from models import Stock
from serializers import StockIn, StockOut, StockUpdate
from starlette.responses import RedirectResponse
from utils import random_market_values, create_tables

from pydantic.error_wrappers import ValidationError
from pynamodb.exceptions import DoesNotExist, DeleteError
from fastapi import Depends, Response, FastAPI, HTTPException, status

app = FastAPI()


@app.get("/")
async def root():
    response = RedirectResponse(url='/docs')
    return response


@app.post("/stock/", response_model=StockOut)
async def create_stock(stock_data: StockIn):
    stock_dict = stock_data.dict()
    stock_dict['market_value'] = random_market_values(number=50)

    db_stock = Stock(**stock_dict)
    db_stock.save()

    return db_stock.attribute_values


async def get_stock(stock_id: str):
    try:
        stock = Stock.get(stock_id)
        return stock
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")


@app.patch("/stock/{stock_id}", response_model=StockOut)
async def update_stock(stock_data: StockUpdate, stock: str = Depends(get_stock)):
    patch_values = stock_data.dict(exclude_defaults=True)
    data = stock.attribute_values

    for key in patch_values.keys():
        data[key] = patch_values[key]

    try:
        StockIn(**data)
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=json.loads(error.json()))

    for k, v in patch_values.items():
        setattr(stock, k, v)

    return stock.attribute_values


@app.get("/stock/{stock_id}", response_model=StockOut)
async def get_stock_by_id(stock: str = Depends(get_stock)):
    return stock.attribute_values


@app.delete("/stock/{stock_id}")
async def delete_stock_by_id(stock: str = Depends(get_stock)):
    try:
        stock.delete()
    except DeleteError:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Unable to remove element from database")

    return Response(content='Stock successfully deleted', status_code=status.HTTP_200_OK)


@app.get("/stocks/")
async def get_stocks_list():
    stocks_data = Stock.scan()
    stocks = [stock.attribute_values for stock in stocks_data]

    return stocks

create_tables()
# handler = Mangum(app)
