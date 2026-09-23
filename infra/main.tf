terraform {
  backend "s3" {
    bucket       = "terraform-locks-1447"
    key          = "global/multistage-photo-admin"
    region       = "us-east-1"
    use_lockfile = true
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "media_bucket" {
  bucket = "multistage-photo-admin-media-bucket"
}

# This bucket won't be used through CloudFront.
# IThis is also required for the S3 bucket policy not to be blocked.
resource "aws_s3_bucket_public_access_block" "allow_public" {
  bucket = aws_s3_bucket.media_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "allow_external_access" {
  bucket = aws_s3_bucket.media_bucket.id
  policy = data.aws_iam_policy_document.allow_access_from_another_account.json

  depends_on = [ aws_s3_bucket_public_access_block.allow_public ]
}

data "aws_iam_policy_document" "allow_access_from_another_account" {
  statement {
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.media_bucket.arn,
      "${aws_s3_bucket.media_bucket.arn}/*",
    ]
  }
}

output "aws_s3_bucket_id" {
  value = aws_s3_bucket.media_bucket.id
}

