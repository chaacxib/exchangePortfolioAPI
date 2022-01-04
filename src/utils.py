from faker import Faker
from src.models import Stock


def random_market_values(number=50):
    """Create a list of random float market values

    Args:
        number (int, optional): Number of values to create. Defaults to 50.

    Returns:
        List[float]: List of market values
    """
    fake = Faker()

    values = [float(fake.pricetag().replace('$', '').replace(',', '')) for _ in range(number)]
    return values


def create_tables():
    """Create database tables if not created yet.
    """
    if not Stock.exists():
        Stock.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
