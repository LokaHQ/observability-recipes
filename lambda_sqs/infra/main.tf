provider "aws" {
  region = "eu-central-1"
}

resource "aws_sqs_queue" "standard_queue" {
    name = "StandardSQSQueue"

    visibility_timeout_seconds = 30
    message_retention_seconds = 600
}


resource "aws_lambda_function" "producer_lambda" {
    function_name = "ProducerLambda"
    role = aws_iam_role.lambda_producer_role.arn
    handler = "lambda_function.lambda_handler"
    runtime = "python3.11"
    filename = "../app/producer/lambda_function.zip"
    source_code_hash = filebase64sha256("../app/producer/lambda_function.zip")

    tracing_config {
        mode = "Active"
    }

    environment {
        variables = {
            QUEUE_URL = aws_sqs_queue.standard_queue.id,
            AWS_LAMBDA_EXEC_WRAPPER = "/opt/otel-instrument"

        }
    }

    layers = [
        "arn:aws:lambda:eu-central-1:901920570463:layer:aws-otel-python-amd64-ver-1-17-0:1"
    ]
}

resource "aws_lambda_function" "consumer_lambda" {
    function_name = "ConsumerLambda"
    role = aws_iam_role.lambda_consumer_role.arn
    handler = "lambda_function.lambda_handler"
    runtime = "python3.11"
    filename = "../app/consumer/lambda_function.zip"
    source_code_hash = filebase64sha256("../app/consumer/lambda_function.zip")

    tracing_config {
        mode = "Active"
    }

    environment {
        variables = {
            AWS_LAMBDA_EXEC_WRAPPER = "/opt/otel-instrument"
        }
    }

    layers = [
        "arn:aws:lambda:eu-central-1:901920570463:layer:aws-otel-python-amd64-ver-1-17-0:1"
    ]
}

resource "aws_lambda_event_source_mapping" "sqs_trigger_consumer_lambda" {
    event_source_arn = aws_sqs_queue.standard_queue.arn
    function_name = aws_lambda_function.consumer_lambda.arn
    batch_size = 1
    enabled = true
}

