from opentelemetry import trace


tracer = trace.get_tracer(__name__)


@tracer.start_as_current_span("consume_message")
def lambda_handler(event, context):
    print(event)