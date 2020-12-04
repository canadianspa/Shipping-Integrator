from .builders.quotes_builder import build_quotes
from .builders.consignment_builder import consignment_builder
from .api import (
    create_consignment,
    delete_consignment,
    get_labels,
)


def build_dx_quotes():
    quotes = build_quotes()

    return quotes, 201


def create_dx_shipment(shipment):
    consignment = consignment_builder(shipment)

    response = create_consignment(consignment)

    if response["Status"] == 0:
        consignment_number = response["ConsignmentNumber"]

        label = get_labels(consignment_number)

        return ({"label": label, "tracking_number": consignment_number}, 201)
    else:
        return ({"message": response["StatusMessage"]}, 500)


def delete_dx_shipment(consignment_number):
    response = delete_consignment(consignment_number)

    if response["Status"] == 0:
        return ("", 204)
    else:
        return ({"message": response["StatusMessage"]}, 500)
