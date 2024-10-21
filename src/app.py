from random import randint
from flask import Flask, request
import logging

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.trace import get_tracer_provider, set_tracer_provider

# initialize otel traces and span
set_tracer_provider(TracerProvider())
get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)

# set instrumentor to automatically instrument flask app
instrumentor = FlaskInstrumentor()
app = Flask(__name__)

# tell isntrumentor to instrument flask app
instrumentor.instrument_app(app)
# optionally exclude certain urls
# instrumentor.instrument_app(app, excluded_urls="/server_request")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/roll")
def roll_dice():
    player = request.args.get('player', default=None, type=str)
    result = str(rolldice())
    if player:
        logger.warning("%s is rolling the dice: %s", player, result)
    else:
        logger.warning("Anonymous player is rolling the dice: %s", result)
    return result

@app.route("/")
def hello_world():
    return "Hello, World!"


def rolldice():
    return randint(1, 6)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
    print("test")