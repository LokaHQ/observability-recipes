from opentelemetry import trace
import json


tracer = trace.get_tracer(__name__)


@tracer.start_as_current_span("consume_messages")
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": "Message read"
}
