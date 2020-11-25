from flask import Flask, request, jsonify

from middleware.auth import authenticate
from common.credentials.tokens import VEEQO_REQUEST_TOKEN
from strategies.quotes_shipment_strategy import quotes_shipment_strategy
from strategies.create_shipment_strategy import create_shipment_strategy
from strategies.delete_shipment_strategy import delete_shipment_strategy

app = Flask(__name__)

app.wsgi_app = authenticate(app.wsgi_app, VEEQO_REQUEST_TOKEN)


@app.route('/<carrier>/quotes', methods=['POST'])
def quotes(carrier):
    quotes, code = quotes_shipment_strategy(carrier)

    return jsonify(quotes), code


@app.route('/<carrier>/shipments', methods=['POST'])
def create_shipment(carrier):
    shipment = request.json

    response, code = create_shipment_strategy(carrier, shipment)

    return jsonify(response), code


@app.route('/<carrier>/shipments/<tracking_number>', methods=['DELETE'])
def delete_shipment(carrier, tracking_number):
    response = delete_shipment_strategy(carrier, tracking_number)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=33, debug=True, threaded=True)
