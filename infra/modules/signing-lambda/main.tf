variable "bucket_id" {
  type = string
}

# gets the project files
data "archive_file" "lambda" {
  for_each = toset([
    "get_file", 
    "put_file", 
    "create_project",
    "get_project_list"
    ])

  type        = "zip"
  source_file = "${path.module}/src/${each.key}/index.py"
  output_path = "${path.module}/dist/${each.key}.zip"
}

# allows lambda to assume a role.
resource "aws_iam_role" "this" {
  name = "s3-signing-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# allows `this` role to list inside bucket, and to get,put,delete,abort bucket.
resource "aws_iam_role_policy" "s3" {
  name = "s3-object-access"
  role = aws_iam_role.this.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = "arn:aws:s3:::${var.bucket_id}"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:AbortMultipartUpload",
        ]
        Resource = "arn:aws:s3:::${var.bucket_id}/*"
      },
    ]
  })
}

# Adds basic lambda execution role to s3 signing role
resource "aws_iam_role_policy_attachment" "logs" {
  role       = aws_iam_role.this.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Creates a function from each dist file.
resource "aws_lambda_function" "signing" {
  for_each = data.archive_file.lambda

  function_name    = "s3-signing-${each.key}"
  role             = aws_iam_role.this.arn
  runtime          = "python3.12"
  handler          = "index.handler"
  filename         = each.value.output_path
  source_code_hash = each.value.output_base64sha256

  environment {
    variables = {
      BUCKET = var.bucket_id
    }
  }
}

# Allows Lambda to invoke Api gateway
resource "aws_lambda_permission" "apigw" {
  for_each = aws_lambda_function.signing

  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = each.value.function_name
  principal     = "apigateway.amazonaws.com"
  # source_arn    = "${aws_api_gateway_rest_api.lambdaGWRestApi.execution_arn}/*/*/*"
  source_arn = "${aws_apigatewayv2_api.lambdaGWRestApi.execution_arn}/*/*/*"
}
