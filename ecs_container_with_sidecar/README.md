Instructions:


### Requirements:
- aws cli set
- Docker installed
- terraform installed
- Python 3.12

### Building the image 

First set the environment variables needed to build and push the image. For example

```
export AWS_REGION="eu-central-1"
export AWS_ACCOUNT_ID="123456"
export REGISTRY_NAME="fastapi-app"
export TAG="v1.0"
```

Run `make create_image` - The script will login to ECR, build the docker image, tag it and push the tagged version to ECR.


Define the variables in `infra/terraform.tfvars`:
- vpc_id - VPC in which you will deploy the infrastructure
- public_subnets - list of public subnets in the vpc
- datadog_api_key - API key for your DataDog Account
- datadog_site - base URL for DataDog. Depending on your account it could have different prefixes i.e. us1.datadoghq.com, us5.datadoghq.com or similar
- ecr_image - once you build the FastAPI application container (locally or in a pipline) and push it to ecr, define the image which will then be deployed as an ECS task.


### Deployment 


- `make plan` - to see the planned infrastructure changes without applying them.
- ` make deploy` - to deploy changes 


Important note: This is not a production example. For simplicity, the two tasks (application and open telemetry collector) are deployed in a public subnet and given a public IP address. 
In production environments, they should be deployed in a private subnet. The access to the application
container should be exposed using an Application Load Balancer. The open telemetry sidecar 
would need a NAT gateway to send telemetry to DataDog. 

