from random import randint
from flask import Flask, request
import redis
import time
import logging

from opentelemetry.instrumentation.flask import FlaskInstrumentor

from opentelemetry.exporter.zipkin.proto.http import ZipkinExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.trace import get_tracer_provider, set_tracer_provider, get_tracer

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "test-flask-app"
})

set_tracer_provider(TracerProvider())
tracer = get_tracer(__name__)

# create a ZipkinExporter
zipkin_exporter = ZipkinExporter(
    endpoint="http://zipkin-service:9411/api/v2/spans",
    # resource=resource,
    # timeout=5 (in seconds),
    # session=requests.Session(),
)

# add span processors to tracer
get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
get_tracer_provider().add_span_processor(
    BatchSpanProcessor(zipkin_exporter)
)



# set instrumentor to automatically instrument flask app
instrumentor = FlaskInstrumentor()
app = Flask(__name__)
Flask

# add redis server to cache results
cache = redis.Redis(host='redis', port=6379)

# tell isntrumentor to instrument flask app
instrumentor.instrument_app(app)
# optionally exclude certain urls
# instrumentor.instrument_app(app, excluded_urls="/server_request")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_hit_count():
    retries = 5
    while True:
        try:
            logger.info('trying to increase hits')
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            logger.info(f'Redis Connection error, {retries} retries left')
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

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
    with tracer.start_as_current_span("test-span"):
        count = get_hit_count()
        logger.info(f"count equals {count}")
        return f"Hello, World! I have been seen {count} times."


def rolldice():
    return randint(1, 6)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
    print("test")