from common.utils import class_to_json
from classes.quote import Quote

DROPOFF = "dropoff"


def build_xdp_quotes():
    quotes = [
        Quote("Parcel - Overnight", "O/N", DROPOFF),
        Quote("Parcel - Economy", "ECON", DROPOFF),
        Quote("Parcel - 12pm", "1200", DROPOFF),
        Quote("Parcel - Sat 12pm", "S12", DROPOFF),
        Quote("Parcel - Sat 10.30am", "S10", DROPOFF),
    ]

    return class_to_json(quotes), 201
