## AWS observability recipes 

### Prerequisites 

- terraform
- aws cli v2

Recipes:
1. lambda_sqs: Two lambda functions communicating through an SQS queue. Example simulates a temperature measurement
being sent to the SQS queue. A custom metric is created. The average value over time is displayed in 
a custom CloudWatch dashboard. OpenTelemetry layer used for observability.
Traces are exported to X-Ray.