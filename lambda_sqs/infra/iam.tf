resource "aws_iam_role" "lambda_producer_role" {
    name = "lambda_observability_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [{
            Effect = "Allow",
            Principal = {
                Service = "lambda.amazonaws.com"
            },
            Action = "sts:AssumeRole"
        }]
    })
}

resource "aws_iam_role_policy" "sqs_producer_lambda_policy" {
    name = "sqs_producer_lambda_policy"
    role = aws_iam_role.lambda_producer_role.id

    policy = jsonencode({
        Version = "2012-10-17",
        Statement = [{
            Effect = "Allow",
            Action = ["sqs:SendMessage"],
            Resource = aws_sqs_queue.standard_queue.arn
        },
        {
            Effect = "Allow",
            Action = [
                "logs:CreateLogGroup", 
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            Resource = "arn:aws:logs:*:*:*"
        },
        {
            Effect = "Allow",
            Action = [
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords"
            ],
            Resource = "*"
        }
        ]
    })
}

resource "aws_iam_role" "lambda_consumer_role" {
    name = "lambda_observability_consumer_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [{
            Effect = "Allow",
            Principal = {
                Service = "lambda.amazonaws.com"
            },
            Action = "sts:AssumeRole"
        }]
    })
}

resource "aws_iam_role_policy" "sqs_consumer_lambda_policy" {
    name = "sqs_consumer_lambda_policy"
    role = aws_iam_role.lambda_consumer_role.id

    policy = jsonencode({
        Version = "2012-10-17",
        Statement = [{
            Effect = "Allow",
            Action = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"],
            Resource = aws_sqs_queue.standard_queue.arn
        },
        {
            Effect = "Allow",
            Action = [
                "logs:CreateLogGroup", 
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            Resource = "arn:aws:logs:*:*:*"
        },
        {
            Effect = "Allow",
            Action = [
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords"
            ],
            Resource = "*"
        }
        ]
    })
}