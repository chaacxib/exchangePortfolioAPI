from collections import Counter
from fastapi.testclient import TestClient

from src.main import app
from src.models import Stock
from src.serializers import StockOut
from pynamodb.exceptions import DoesNotExist

VALIDATOR_ERRORS = [
    'field limited to 10 characters',
    'field limited to 50 characters',
    'field limited to 100 characters',
]

client = TestClient(app)

def get_stocks_from_db():
        stocks_data = Stock.scan()
        stocks = [stock.attribute_values for stock in stocks_data]
        return stocks



def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_create_stock(faker):
    # Field validators
    response = client.post(
        url="/stock/",
        json={
            "name": faker.pystr(min_chars=50, max_chars=100),
            "description": faker.pystr(min_chars=100, max_chars=110),
            "symbol": faker.pystr(min_chars=10, max_chars=15)
        }
    )
    data = response.json()

    assert response.status_code == 422

    assert 'detail' in data.keys()
    assert isinstance(data['detail'], list)
    assert len(data['detail']) == 3

    assert Counter(VALIDATOR_ERRORS) == Counter([error['msg'] for error in data['detail']])

    # Real stock company symbol validator
    response = client.post(
        url="/stock/",
        json={
            "name": faker.pystr(min_chars=1, max_chars=50),
            "description": faker.pystr(min_chars=1, max_chars=100),
            "symbol": faker.pystr(min_chars=1, max_chars=10)
        }
    )
    data = response.json()

    assert response.status_code == 422

    assert 'detail' in data.keys()
    assert isinstance(data['detail'], list)
    assert len(data['detail']) == 1

    assert  data['detail'][0]['msg'] == 'symbol not listed in the New York stock exchange'

    # Successfull call
    response = client.post(
        url="/stock/",
        json={
            "name": 'Vanguard S&P 500 ETF',
            "description": 'Track the performance of the Standard & Pooras 500 Index',
            "symbol": 'VOO'
        }
    )
    data = response.json()

    assert response.status_code == 200
    assert StockOut.validate(data)

    assert Stock.get(data['id']).exists()
    

def test_get_stock_by_id():
    stock = get_stocks_from_db().pop(0)
    response = client.get(url=f"/stock/{stock['id']}")
    data = response.json()

    assert response.status_code == 200
    assert StockOut.validate(data)


def test_delete_stock_by_id():
    stock = get_stocks_from_db().pop(0)
    response = client.delete(url=f"/stock/{stock['id']}")

    assert response.status_code == 200
    assert response.text == 'Stock successfully deleted'

    try:
        assert not Stock.get(stock['id']).exists()
    except Exception as error:
        assert isinstance(error, DoesNotExist)


def test_update_stock():
    stock = get_stocks_from_db().pop(0)
    response = client.patch(
        url=f"/stock/{stock['id']}",
        json={
            "name": 'Updated',
        }
    )
    data = response.json()
    updated_stock = Stock.get(stock['id'])
    updated_stock.refresh()

    assert response.status_code == 200
    assert StockOut.validate(data)

    assert data['name'] == 'Updated'
    assert updated_stock.name == data['name']


def test_get_stocks_list():
    stocks = get_stocks_from_db()
    response = client.get(url=f"/stocks/")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(stocks) == len(data)
    assert all(StockOut.validate(stock) for stock in data)
