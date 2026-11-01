resource "aws_dynamodb_table" "project_table" {
  name             = "project-table-terraform-mikolertesx"
  hash_key         = "projectNameKey"
  billing_mode     = "PAY_PER_REQUEST"

  attribute {
    name = "projectNameKey"
    type = "S"
  }
}

output "dynamodb_id" {
  value = aws_dynamodb_table.project_table.id
}

output "dynamodb_name" {
  value = aws_dynamodb_table.project_table.name
}

output "dynamodb_arn" {
  value = aws_dynamodb_table.project_table.arn
}

