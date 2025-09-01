variable "vpc_id" {
  type        = string
  description = "ID of the VPC in your account"
}


variable "public_subnets" {
  type        = list(string)
  description = "list of public subnets"
}

variable "datadog_api_key" {
  type        = string
  sensitive   = true
  description = "Your DataDog API key"
}

variable "datadog_site" {
  type        = string
  description = "DataDog base URL"
}

variable "region" {
  type        = string
  description = "Preferred AWS region"
}

variable "ecr_image" {
  type        = string
  description = "Your FastAPI application image on ECR"
}