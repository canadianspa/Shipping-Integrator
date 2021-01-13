from flask import Flask, request, redirect, jsonify
import json

from middleware.auth import authenticate
from common.credentials.tokens import VEEQO_REQUEST_TOKEN

from carriers.utils import handle_shipment, get_carrier
from builders.quotes import build_quotes
from strategies.create_shipment_strategy import create_shipment_strategy
from strategies.delete_shipment_strategy import delete_shipment_strategy
from strategies.track_shipment_strategy import track_shipment_strategy

app = Flask(__name__)

app.wsgi_app = authenticate(app.wsgi_app, VEEQO_REQUEST_TOKEN)


@app.route("/quotes", methods=["POST"])
def quotes():
    quotes = build_quotes()

    return jsonify(quotes), 201


@app.route("/shipments", methods=["POST"])
def create_shipment():
    _shipment = request.json

    carrier, shipment = handle_shipment(_shipment)

    response, code = create_shipment_strategy(carrier, shipment)

    return jsonify(response), code


@app.route("/shipments/<tracking_number>", methods=["DELETE"])
def delete_shipment(tracking_number):
    carrier = get_carrier(tracking_number)

    response = delete_shipment_strategy(carrier, tracking_number)

    return response


@app.route("/tracking", methods=["GET"])
def track_shipment():
    tracking_number = request.args.get("id")

    carrier = get_carrier(tracking_number)

    url = track_shipment_strategy(carrier, tracking_number)

    return redirect(url, code=302)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=33, debug=True, threaded=True)
