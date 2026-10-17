# Copyright IBM Corp. 2014, 2026
# SPDX-License-Identifier: MPL-2.0

locals {
  routes = {
    for name, fn in aws_lambda_function.signing : name => {
      path   = name
      method = "GET"
      uri    = fn.invoke_arn
    }
  }
}

resource "aws_apigatewayv2_api" "lambdaGWRestApi" {
  name          = "Signin-Lambda URL"
  protocol_type = "HTTP"
}

# DeploymentID is optional because you can set it to auto_deploy instead.
resource "aws_apigatewayv2_stage" "developmentStage" {
  api_id        = aws_apigatewayv2_api.lambdaGWRestApi.id
  name          = "development"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  for_each = aws_lambda_function.signing

  api_id           = aws_apigatewayv2_api.lambdaGWRestApi.id
  integration_type = "AWS_PROXY"

  integration_method = "POST"
  integration_uri = aws_lambda_function.signing[each.key].invoke_arn
}

resource "aws_apigatewayv2_route" "lambda_execution_route" {
  for_each = aws_lambda_function.signing

  api_id    = aws_apigatewayv2_api.lambdaGWRestApi.id
  route_key = "GET /${each.key}"

  target = "integrations/${aws_apigatewayv2_integration.lambda_integration[each.key].id}"
}

output "apigateway_url" {
    value = aws_apigatewayv2_stage.developmentStage.invoke_url
}
