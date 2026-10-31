# aws dynamodb create-table \
#     --table-name Music \
#     --attribute-definitions \
#         AttributeName=Artist,AttributeType=S \
#         AttributeName=SongTitle,AttributeType=S \
#     --key-schema \
#         AttributeName=Artist,KeyType=HASH \
#         AttributeName=SongTitle,KeyType=RANGE \
#     --billing-mode=PAY_PER_REQUEST

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

