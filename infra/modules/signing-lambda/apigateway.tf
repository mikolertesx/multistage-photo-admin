# Copyright IBM Corp. 2014, 2026
# SPDX-License-Identifier: MPL-2.0

resource "aws_api_gateway_rest_api" "lambdaGWRestApi" {
  name = "Signin-Lambda URL"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_deployment" "lambdaGWRestApiDeployment" {
  rest_api_id = aws_api_gateway_rest_api.lambdaGWRestApi.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.signing,
      aws_api_gateway_method.signing,
      aws_api_gateway_integration.get_signin_method_integration
    ]))
  }

  depends_on = [ 
     aws_api_gateway_integration.get_signin_method_integration,
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "developmentStage" {
  rest_api_id   = aws_api_gateway_rest_api.lambdaGWRestApi.id
  deployment_id = aws_api_gateway_deployment.lambdaGWRestApiDeployment.id
  stage_name    = "dev"
}

resource "aws_api_gateway_method_settings" "example" {
  rest_api_id = aws_api_gateway_rest_api.lambdaGWRestApi.id
  stage_name  = aws_api_gateway_stage.developmentStage.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled = true
  }
}

resource "aws_api_gateway_integration" "get_signin_method_integration" {
  for_each = aws_api_gateway_method.signing

  rest_api_id = aws_api_gateway_rest_api.lambdaGWRestApi.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.signing[each.key].invoke_arn
}

resource "aws_api_gateway_resource" "signing" {
  for_each = aws_lambda_function.signing

  rest_api_id = aws_api_gateway_rest_api.lambdaGWRestApi.id
  parent_id = aws_api_gateway_rest_api.lambdaGWRestApi.root_resource_id

  path_part = each.key
}

resource "aws_api_gateway_method" "signing" {
  for_each = aws_api_gateway_resource.signing

  rest_api_id = aws_api_gateway_rest_api.lambdaGWRestApi.id
  resource_id = each.value.id
  http_method = "GET"
  authorization = "NONE"
}

output "apigateway_url" {
    value = aws_api_gateway_stage.developmentStage.invoke_url
}

