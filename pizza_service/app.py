import json

from flask import Flask
import service

app = Flask(__name__)


@app.route("/order/<count>", methods=["POST"])
def order_pizzas(count):
    order_id = service.order_pizzas(int(count))
    return json.dumps({"order_id": order_id})
