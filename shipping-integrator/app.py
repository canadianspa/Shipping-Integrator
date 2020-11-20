from flask import Flask, request, jsonify

from common.credentials.tokens import VEEQO_REQUEST_TOKEN
from middleware.auth import authenticate
from common.utils import class_to_json


from classes.service_factory import ServiceFactory

app = Flask(__name__, static_folder='./', static_url_path='/')

app.wsgi_app = authenticate(app.wsgi_app, VEEQO_REQUEST_TOKEN)


@app.route('/<carrier>/quotes',  methods=['POST'])
def quotes(carrier):
    quotes = ServiceFactory(carrier)
    quotes_json = class_to_json(quotes)

    return jsonify(quotes_json)


@app.route('/<carrier>/shipments',  methods=['POST'])
def create_shipment(carrier):
    print(carrier)
    return jsonify([])


@app.route('/<carrier>/shipments/<tracking_number>',  methods=['DELETE'])
def delete_shipment(carrier, tracking_number):
    print(carrier, tracking_number)
    return jsonify([])


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
