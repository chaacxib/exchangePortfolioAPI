from faker import Faker
from models import Stock


def random_market_values(number=50):
    fake = Faker()

    values = [float(fake.pricetag().replace('$', '').replace(',', '')) for _ in range(number)]
    return values


def create_tables():
    if not Stock.exists():
        Stock.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
