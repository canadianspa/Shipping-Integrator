from common.utils import class_to_json
from classes.quote import Quote


def build_quotes():
    DROPOFF = "dropoff"

    quotes = [
        Quote("1man - Overnight", "ON", DROPOFF),
        Quote("1man - Overnight 9:30", "930", DROPOFF),
        Quote("1man - Overnight pre-noon", "AM", DROPOFF),
        Quote("1man - 3Day", "3D", DROPOFF),
        Quote("1man - Saturday", "SAT", DROPOFF),
        Quote("1man - Saturday 9:30", "S93", DROPOFF),
    ]

    return class_to_json(quotes)
