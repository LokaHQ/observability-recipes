Instructions:


Requirements:
- aws cli set
- Docker installed
- terraform installed
- Python 3.12


Define the variables in `infra/terraform.tfvars`:
- vpc_id - VPC in which you will deploy the infrastructure
- public_subnets - list of public subnets in the vpc
- datadog_api_key - API key for your DataDog Account
- datadog_site - base URL for DataDog. Depending on your account it could have different prefixes i.e. us1.datadoghq.com, us5.datadoghq.com or similar
- ecr_image - once you build the FastAPI application container (locally or in a pipline) and push it to ecr, define the image which will then be deployed as an ECS task.

Important note: This is not a production example. For simplicity, the two tasks (application and open telemetry collector) are deployed in a public subnet and given a public IP address. 
In production environments, they should be deployed in a private subnet. The access to the application
container should be exposed using an Application Load Balancer. The open telemetry sidecar 
would need a NAT gateway to send telemetry to DataDog. 

