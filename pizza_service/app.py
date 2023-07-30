import json

from flask import Flask
from pizza_service import service

app = Flask(__name__)


@app.route("/order/<count>", methods=["POST"])
def order_pizzas(count):
    order_id = service.order_pizzas(int(count))
    return json.dumps({"order_id": order_id})


@app.route("/order/<order_id>", methods=["GET"])
def get_order(order_id):
    return service.get_order(order_id)
