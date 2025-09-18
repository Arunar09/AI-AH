#!/bin/bash
# Terraform Test Script

set -e

echo "🧪 Testing Terraform configuration..."

# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Plan deployment
terraform plan -out=tfplan

# Apply if dry-run is not specified
if [ "$1" != "--dry-run" ]; then
    echo "🚀 Applying Terraform configuration..."
    terraform apply tfplan
    
    # Get outputs
    echo "📊 Terraform outputs:"
    terraform output
    
    # Test connectivity
    echo "🔍 Testing connectivity..."
    if command -v curl &> /dev/null; then
        # Get public IP from output
        PUBLIC_IP=$(terraform output -raw web_public_ip 2>/dev/null || echo "")
        if [ ! -z "$PUBLIC_IP" ]; then
            echo "Testing HTTP connectivity to $PUBLIC_IP..."
            curl -f http://$PUBLIC_IP || echo "❌ HTTP test failed"
        fi
    fi
else
    echo "✅ Dry run completed successfully"
fi
