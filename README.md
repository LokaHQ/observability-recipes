## AWS observability recipes 

### Prerequisites 

- terraform
- aws cli v2

Recipes:
1. lambda_sqs: Two lambda functions communicating through an SQS queue. Example simulates a temperature measurement
being sent to the SQS queue. A custom metric is created. The average value over time is displayed in 
a custom CloudWatch dashboard. OpenTelemetry layer used for observability.
Traces are exported to X-Ray.
2. ecs_container_with_sidecar: A simple Fast API application which sends telemetry data to a OTel collector deployed as a sidecar. Two exporters are defined, one exports data to Cloudwatch, the other to DataDog. This illustates how the application code does not need changes, so you
could easily switch from one to the other, by editing the otel-config.yaml. 