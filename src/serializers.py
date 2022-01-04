import uuid
import requests

from typing import Optional, List
from pydantic import BaseModel, Field, validator
from src.settings import YH_FINANCE_API_SUMMARY_URL, YH_FINANCE_API_HEADERS


class StockIn(BaseModel):
    """Pydantic Model used to create an stock in the database

    Raises:
        ValueError: field limited to 50 characters
        ValueError: field limited to 100 characters
        ValueError: field limited to 10 characters
        ValueError: symbol not listed in the New York stock exchange
    """
    name: str = Field(..., description='Human readable name of the stock company (Max 50 characters)')
    description: str = Field(..., description='Brief description of the stock company (Max 100 characters)')
    symbol: str = Field(..., description='Valid company symbol registered in the New York stock exchange (Max 10 characters)')

    @validator('name')
    def company_name_validator(cls, v):
        if len(v) > 50:
            raise ValueError('field limited to 50 characters')
        return v.title()

    @validator('description')
    def company_description_validator(cls, v):
        if len(v) > 100:
            raise ValueError('field limited to 100 characters')
        return v

    @validator('symbol')
    def company_symbol_validator(cls, v):
        if len(v) > 10:
            raise ValueError('field limited to 10 characters')

        querystring = {
            "symbol": v,
            "region": "US"
        }

        response = requests.request("GET", YH_FINANCE_API_SUMMARY_URL, headers=YH_FINANCE_API_HEADERS, params=querystring)

        if not response.status_code == 200:
            raise ValueError('symbol not listed in the New York stock exchange')

        return v


class StockOut(StockIn):
    """Pydantic Model used to list an stock in the database
    """
    id: uuid.UUID = Field(..., description='Stock identifier. Default UUID4')
    market_value: List[float] = Field(..., description='List of last 50 market values of the stock')


class StockUpdate(BaseModel):
    """Pydantic Model used to update an stock in the database
    """
    name: Optional[str] = Field(None, description='Human readable name of the stock company (Max 50 characters)')
    description: Optional[str] = Field(None, description='Brief description of the stock company (Max 100 characters)')
    symbol: Optional[str] = Field(None, description='Valid company symbol registered in the New York stock exchange (Max 10 characters)')
