import json
# from mangum import Mangum
from models import Stock
from serializers import StockIn, StockOut, StockUpdate
from utils import random_market_values, create_tables

from pydantic.error_wrappers import ValidationError
from pynamodb.exceptions import DoesNotExist, DeleteError

from fastapi.openapi.utils import get_openapi
from starlette.responses import RedirectResponse
from fastapi import Depends, Response, FastAPI, HTTPException, status

from settings import (
    API_VERSION,
    API_TITLE,
    API_DESCRIPTION
)

app = FastAPI()


@app.get("/")
async def root():
    response = RedirectResponse(url='/docs')
    return response


@app.post("/stock/", response_model=StockOut)
async def create_stock(stock_data: StockIn):
    """Create a new stock on the database

    Args:
        stock_data (StockIn): Data of the stock to be created

    Returns:
        StockOut: The updated stock data
    """
    stock_dict = stock_data.dict()
    stock_dict['market_value'] = random_market_values(number=50)

    db_stock = Stock(**stock_dict)
    db_stock.save()

    return db_stock.attribute_values


async def get_stock(stock_id: str):
    """Collect the desired stock object from the database if exists

    Args:
        stock_id (str): Id of the stock to collect

    Raises:
        HTTPException: Stock not found

    Returns:
        stock: Stock object from the database
    """
    try:
        stock = Stock.get(stock_id)
        return stock
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")


@app.patch("/stock/{stock_id}", response_model=StockOut)
async def update_stock(stock_data: StockUpdate, stock: str = Depends(get_stock)):
    """Updates the defined stock from the database

    Args:
        stock_data (StockUpdate): The desired data to update on the stock
        stock_id (str): Id of the stock to collect

    Raises:
        HTTPException: Validation Error on the new parameters

    Returns:
        StockOut: The updated stock data
    """
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
    """Collects the defined stock from the database

    Args:
        stock_id (str): Id of the stock to collect

    Returns:
        StockOut: The defined stock data
    """
    return stock.attribute_values


@app.delete("/stock/{stock_id}")
async def delete_stock_by_id(stock: str = Depends(get_stock)):
    """Delete the defined stock from the database

    Args:
        stock_id (str): Id of the stock to collect

    Raises:
        HTTPException: Unable to remove element from database

    Returns:
        HTTPResponse: Stock successfully deleted
    """
    try:
        stock.delete()
    except DeleteError:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Unable to remove element from database")

    return Response(content='Stock successfully deleted', status_code=status.HTTP_200_OK)


@app.get("/stocks/")
async def get_stocks_list():
    """Return all the stocks created on the database

    Returns:
        List[StockOut]: List of all the stocks stored on the system
    """
    stocks_data = Stock.scan()
    stocks = [stock.attribute_values for stock in stocks_data]

    return stocks


def custom_openapi():
    openapi_schema = get_openapi(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
create_tables()
# handler = Mangum(app)
