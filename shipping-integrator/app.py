from flask import Flask, request, jsonify
import json

from middleware.auth import authenticate
from common.credentials.tokens import VEEQO_REQUEST_TOKEN

from strategies.quotes_shipment_strategy import quotes_shipment_strategy
from strategies.create_shipment_strategy import create_shipment_strategy
from strategies.delete_shipment_strategy import delete_shipment_strategy

app = Flask(__name__)

app.wsgi_app = authenticate(app.wsgi_app, VEEQO_REQUEST_TOKEN)


@app.route("/quotes", methods=["POST"])
def quotes():
    quotes = (
        quotes_shipment_strategy("xdpa") +
        quotes_shipment_strategy("xdpb") +
        quotes_shipment_strategy("xdpc") +
        quotes_shipment_strategy("dx")
    )

    return jsonify(quotes), 201


@app.route("/shipments", methods=["POST"])
def create_shipment():
    shipment = request.json

    shipment["service_code"] = json.loads(shipment["service_code"])

    carrier = shipment["service_code"]["carrier"]

    response, code = create_shipment_strategy(carrier, shipment)

    return jsonify(response), code


@app.route("/shipments/<tracking_number>", methods=["DELETE"])
def delete_shipment(tracking_number):
    # Tracking no format "xxx: 7X0990X000"
    details = tracking_number.split(": ")

    carrier = details[0]
    tracking_number = details[1]

    response = delete_shipment_strategy(carrier, tracking_number)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=33, debug=True, threaded=True)
