from .builders.quotes_builder import build_quotes
from .api import get_session_key

session_key = get_session_key()
print(session_key)


def build_dx_quotes():
    quotes = build_quotes()

    return quotes, 201


def create_dx_shipment(carrier, shipment):
    print(carrier)


def delete_dx_shipment(carrier, tracking_number):
    print(carrier)
