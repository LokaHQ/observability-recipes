from opentelemetry import trace
from opentelemetry.baggage import get_baggage
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


tracer = trace.get_tracer(__name__)


@tracer.start_as_current_span("consume_messages")
def lambda_handler(event, context):
    for record in event["Records"]:
        # extract message attributes
        msg_attrs = {
            k: v["stringValue"]
            for k, v in record["messageAttributes"].items()
        }


        ctx = TraceContextTextMapPropagator().extract(msg_attrs)
        ctx = W3CBaggagePropagator().extract(msg_attrs, context=ctx)

        user_id = get_baggage("user_id", context=ctx)

        with tracer.start_as_current_span("sqs_processor_lambda", context=ctx):
            print(f"Processing message for user: {user_id}")

    
    return {
        "statusCode": 200,
        "body": "Message read"
}




