import json
import time
import boto3
import os

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

sqs_client = boto3.client("sqs")

@tracer.start_as_current_span("child")
def child_function():
    try:
        sqs_client.send_message(
            QueueUrl=os.environ["QUEUE_URL"],
            MessageBody="Hello"
        )
    except Exception as exc:
        span = trace.get_current_span()
        span.set_status(Status(StatusCode.ERROR, str(exc)))


@tracer.start_as_current_span("parent")
def parent_function():
    child_function()


def lambda_handler(event, context):
    print(event)
    parent_function()
