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
