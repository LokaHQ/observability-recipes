provider "aws" {
  region = "eu-central-1"
}

provider "docker" {}

### variables

variable "vpc_id" {
    default = "vpc-03f0acf4be0078039"
}
variable "private_subnets" {
  type = list(string)
  default = ["subnet-0b8ae00ecebad7708", "subnet-048b86c8f1b8acb86", "subnet-023c3b4e59d38385b" ]
}

variable "datadog_api_key" {
    default = "asdasd"
}
variable "datadog_site" {
  default = "datadoghq.com"
}


###  CloudWatch ###

resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "/ecs/exampleApp"
  retention_in_days = 1
}


resource "aws_ecr_repository" "fastapi" {
  name = "fastapi-app"
}

###############################
## ECS resources ###
###############################

resource "aws_ecs_cluster" "app_cluster" {
  name = "otel-sidecar-cluster"
}

resource "aws_ssm_parameter" "otel_config" {
  name         = "/adot/config"
  type         = "String"
  value        = file("otel-config.yaml")
  description  = "Otel configuration for ECS service"
}

resource "aws_ecs_task_definition" "app_with_sidecar" {
  family                   = "app-otel-sidecar"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "otel-collector"
      image = "public.ecr.aws/aws-observability/aws-otel-collector:latest"
      essential = true
      cpu = 256
      memory = 256
      essential = true
      secrets = [
      {
      name  = "AOT_CONFIG_CONTENT"
      valueFrom = aws_ssm_parameter.otel_config.arn
       }]
      portMappings = [
        {
          containerPort = 4317
          protocol      = "tcp"
        },
        {
          containerPort = 4318
          protocol      = "tcp"
        }
      ]
      environment = [
        {
          name  = "DD_API_KEY"
          value = var.datadog_api_key
        },
        {
          name  = "DD_SITE"
          value = var.datadog_site
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.app_logs.name
          awslogs-region        = "eu-central-1"
          awslogs-stream-prefix = "otel"
        }
      }

    }
  ])
}

resource "aws_ecs_service" "api_service" {
  name            = "app-otel-service"
  cluster         = aws_ecs_cluster.app_cluster.id
  task_definition = aws_ecs_task_definition.app_with_sidecar.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnets
    assign_public_ip = true # set false if NAT
    security_groups  = [aws_security_group.app_sg.id]
  }

}


############################################
# Security Group
############################################
resource "aws_security_group" "app_sg" {
  name   = "app-otel-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

