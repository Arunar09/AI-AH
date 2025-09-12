# MinIO Backend Configuration for Terraform State
# This allows Terraform to use MinIO as a remote state backend

terraform {
  backend "s3" {
    endpoint                    = "http://localhost:9000"
    bucket                      = "terraform-state"
    key                         = "lab/terraform.tfstate"
    region                      = "us-east-1"
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_region_validation      = true
    force_path_style            = true
  }
}

# Configure the MinIO Provider
provider "minio" {
  minio_server   = "localhost:9000"
  minio_user     = "minioadmin"
  minio_password = "minioadmin123"
  minio_ssl      = false
}

# Create S3 bucket for application data
resource "minio_s3_bucket" "app_data" {
  bucket = "ai-ah-app-data"
  acl    = "private"
}

# Create S3 bucket for backups
resource "minio_s3_bucket" "backups" {
  bucket = "ai-ah-backups"
  acl    = "private"
}

# Create S3 bucket for logs
resource "minio_s3_bucket" "logs" {
  bucket = "ai-ah-logs"
  acl    = "private"
}

# Create S3 bucket for AI training data
resource "minio_s3_bucket" "ai_training" {
  bucket = "ai-ah-training-data"
  acl    = "private"
}

# Output bucket information
output "bucket_names" {
  value = {
    app_data    = minio_s3_bucket.app_data.bucket
    backups     = minio_s3_bucket.backups.bucket
    logs        = minio_s3_bucket.logs.bucket
    ai_training = minio_s3_bucket.ai_training.bucket
  }
}

output "minio_endpoint" {
  value = "http://localhost:9000"
}
