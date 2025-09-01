from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()

# Define resource with service name
resource = Resource.create({
    SERVICE_NAME: "my-fastapi-app"
})

# Set up tracer provider
provider = TracerProvider(resource=resource)

# Configure OTLP exporter to talk to the sidecar
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",
    insecure=True
)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Set global provider
trace.set_tracer_provider(provider)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

@app.get("/health-check")
def index():
    return {"status": "OK"}
