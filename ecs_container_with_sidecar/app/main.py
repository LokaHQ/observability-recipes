from fastapi import FastAPI
from opentelemetry import trace, metrics
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
import boto3
import json
import os
from typing import Dict

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


@app.get("/health-check")
def index():
    return {"status": "OK"}


@app.post("/messages")
def message(payload: Dict[str, str]):
    sqs_client.send_message(
        QueueUrl=os.environ["QUEUE_URL"], MessageBody=json.dumps(payload)
    )
    return {"status": "SENT"}
