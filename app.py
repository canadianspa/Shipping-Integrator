from flask import Flask, request, jsonify
import json

from middleware.auth import authenticate
from common.credentials import VEEQO_REQUEST_TOKEN

from carriers.xdp.carrier import XDP
from carriers.dx.carrier import DX
from carriers.panther.carrier import Panther
from carriers.utils import parse_tracking_string


app = Flask(__name__)
app.wsgi_app = authenticate(app.wsgi_app, VEEQO_REQUEST_TOKEN)


# Edit to change environment of certain carriers
xdp = XDP(testing=False)
dx = DX(testing=False)
panther = Panther(testing=True)


@app.route("/quotes", methods=["POST"])
def quotes():
    quotes = xdp.quotes() + dx.quotes() + panther.quotes()

    return jsonify(quotes), 201


@app.route("/shipments", methods=["POST"])
def create():
    shipment = request.json

    details = json.loads(shipment["service_code"])

    carrier = details["carrier"]
    service_code = details["code"]

    if "xdp" in carrier:
        return xdp.create(carrier, service_code, shipment)
    elif carrier == "dx":
        return dx.create(service_code, shipment)
    elif carrier == "panther":
        return panther.create(service_code, shipment)

    raise Exception("Invalid carrier: " + carrier)


@app.route("/shipments/<tracking_string>", methods=["DELETE"])
def delete(tracking_string):
    carrier, tracking_number = parse_tracking_string(tracking_string)

    if "xdp" in carrier:
        return xdp.delete(tracking_number)
    elif carrier == "dx":
        return dx.delete(tracking_number)
    elif carrier == "panther":
        return panther.delete(tracking_number)

    raise Exception("Invalid carrier: " + carrier)


@app.route("/tracking", methods=["GET"])
def track():
    tracking_string = request.args.get("id")

    carrier, tracking_number = parse_tracking_string(tracking_string)

    if "xdp" in carrier:
        return xdp.track(tracking_number)
    elif carrier == "dx":
        return dx.track(tracking_number)
    elif carrier == "panther":
        return panther.track(tracking_number)

    raise Exception("Invalid carrier: " + carrier)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=33,
        debug=True,
        threaded=True,
    )
