from fastapi import FastAPI
from opentelemetry import trace, metrics, baggage, context
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import boto3
import json
import os
from typing import Dict
from uuid import uuid4

sqs_client = boto3.client("sqs")

app = FastAPI()

# Define resource with service name
resource = Resource.create({SERVICE_NAME: "my-fastapi-app"})


# Configure OTLP exporter to talk to the sidecar
# It will send traces in OTLP format to the collector running on port 4317
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)


span_processor = BatchSpanProcessor(otlp_exporter)
trace.set_tracer_provider(
    TracerProvider(
        resource=resource,
        active_span_processor=span_processor,
        id_generator=AwsXRayIdGenerator(),
    )
)


## Setup metrics export
metric_exporter = OTLPMetricExporter()
metric_reader = PeriodicExportingMetricReader(exporter=metric_exporter)
metric_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(metric_provider)


# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)
BotocoreInstrumentor().instrument()

tracer = trace.get_tracer(__name__)


@app.get("/health-check")
def index():
    return {"status": "OK"}


@app.post("/messages")
def message(payload: Dict[str, str]):
    # let's simulate a scenario where we're propagating the ID of the logged in user
    ctx = baggage.set_baggage("user_id", str(uuid4()))

    message_attributes = {}
    TraceContextTextMapPropagator().inject(message_attributes, context=ctx)
    W3CBaggagePropagator().inject(message_attributes, context=ctx)

    sqs_attributes = {
        k: {"StringValue": v, "DataType": "String"}
        for k, v in message_attributes.items()
    }

    with tracer.start_as_current_span("send_sqs_message"):
        sqs_client.send_message(
            QueueUrl=os.environ["QUEUE_URL"],
            MessageBody=json.dumps(payload),
            MessageAttributes=sqs_attributes,
        )
        return {"status": "SENT"}
