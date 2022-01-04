import uuid

from settings import ON_CLOUD
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberSetAttribute


# UUID  Attribute will use as Dynamo hash key
class UUIDAttribute(UnicodeAttribute):

    def serialize(self, value):
        return super().serialize(str(value))

    def deserialize(self, value):
        return uuid.UUID(super().deserialize(value))


class Stock(Model):
    """Stock Model on the database to store and manipulate the stocks generated on the API endpoints

    Fields:
        id (UUID): Stock identifier
        name (str): Human readable name of the stock company
        description (str): Brief description of the stock company
        symbol (str): Valid company symbol registered in the New York stock exchange
        market_value (List[float]): List of last 50 market values of the stock
    """
    class Meta:
        table_name = 'portfolio-stocks'
        region = 'us-east-1'

        if not ON_CLOUD:
            host = "http://localhost:4567"

    id = UUIDAttribute(hash_key=True, default=uuid.uuid4)
    name = UnicodeAttribute()
    description = UnicodeAttribute()
    symbol = UnicodeAttribute()
    market_value = NumberSetAttribute()
