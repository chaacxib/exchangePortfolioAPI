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
    """
    A DynamoDB User
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
