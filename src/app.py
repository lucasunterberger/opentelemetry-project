from random import randint
from flask import Flask, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/rolldice")
def roll_dice():
    player = request.args.get('player', default=None, type=str)
    result = str(roll())
    if player:
        logger.warning("%s is rolling the dice: %s", player, result)
    else:
        logger.warning("Anonymous player is rolling the dice: %s", result)
    return result

@app.route("/")
def hello_world():
    return "Hello, World!"


def roll():
    return randint(1, 6)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
    print("test")