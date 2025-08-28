from opentelemetry import trace, metrics
from opentelemetry.sdk.metrics import MeterProvider
import json


provider = MeterProvider()
metrics.set_meter_provider(provider)

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

temperature_histogram = meter.create_histogram(
    name = "temperature",
    unit = "C",
    description = "Temperature reading"
)


def extract_reading(event):
    for record in event['Records']:
        message_body = json.loads(record["body"])
        temp = message_body.get("temperature")
        if temp is not None:
            yield float(temp)


@tracer.start_as_current_span("consume_messages")
def lambda_handler(event, context):
    for reading in extract_reading(event):
        with tracer.start_as_current_span("record_temperature") as span:
            temperature_histogram.record(reading)

    return {
        "statusCode": 200,
        "body": "Data processed"
}
