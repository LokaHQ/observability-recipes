import json
import boto3
import os
import random

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

sqs_client = boto3.client("sqs")

@tracer.start_as_current_span("send_to_sqs")
def send_to_sqs(payload):
    try:
        sqs_client.send_message(
            QueueUrl=os.environ["QUEUE_URL"],
            MessageBody=json.dumps(payload)
        )
    except Exception as exc:
        span = trace.get_current_span()
        span.set_status(Status(StatusCode.ERROR, str(exc)))
        raise


@tracer.start_as_current_span("produce_message")
def lambda_handler(event, context):
    reading = {
        "temperature": random.uniform(25,30),
    }
    send_to_sqs(reading)

    return {
        "statusCode": 200,
        "body": "Message sent"
}
