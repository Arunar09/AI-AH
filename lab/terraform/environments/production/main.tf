# Production-like Environment
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Module
module "vpc" {
  source = "../../modules/vpc"
  
  name        = "production"
  environment = var.environment
  cidr_block  = var.vpc_cidr
  
  availability_zones = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
}

# EC2 Module
module "web_servers" {
  source = "../../modules/ec2"
  
  name        = "production-web"
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.public_subnet_ids
  
  instance_count = var.web_instance_count
  instance_type  = var.web_instance_type
  allowed_ports  = [22, 80, 443]
  
  user_data = file("${path.module}/user_data.sh")
}
