# AI-AH Local Lab Environment

This directory contains a comprehensive local lab setup for testing and validating AI-AH agents against real infrastructure deployments.

## 🏗️ Lab Architecture

The lab provides three environments for testing:

### 1. **Basic Environment**
- Simple web application with database
- Services: web, database, load_balancer
- Perfect for initial testing and validation

### 2. **Advanced Environment**
- Microservices architecture with monitoring
- Services: api, auth, database, cache, queue, monitoring
- Tests complex infrastructure patterns

### 3. **Production Environment**
- Production-ready infrastructure
- Services: web, api, database, cache, queue, monitoring, logging
- Validates enterprise-grade deployments

## 🚀 Quick Start

### 1. Setup Lab Environment
```bash
# Run the lab setup
python lab/setup_local_lab.py

# Or use the lab runner
python lab/run_lab.py setup
```

### 2. Test Agents (Dry Run)
```bash
# Test without creating real resources
python lab/run_lab.py test --environment basic --dry-run

# Run comprehensive agent tests
python lab/test_agents.py
```

### 3. Deploy to AWS (Real Resources)
```bash
# Deploy basic environment
python lab/run_lab.py deploy --environment basic

# Deploy with dry-run first
python lab/run_lab.py deploy --environment advanced --dry-run
```

### 4. Cleanup Resources
```bash
# Clean up resources
python lab/run_lab.py cleanup --environment basic
```

## 📁 Directory Structure

```
lab/
├── setup_local_lab.py          # Main setup script
├── run_lab.py                  # Lab runner script
├── test_agents.py              # Agent test framework
├── test_terraform.sh           # Terraform validation script
├── test_docker.sh              # Docker validation script
├── terraform/
│   ├── modules/                # Reusable Terraform modules
│   │   ├── vpc/               # VPC module
│   │   └── ec2/               # EC2 module
│   └── environments/           # Environment configurations
│       ├── basic/             # Basic environment
│       ├── advanced/          # Advanced environment
│       └── production/        # Production environment
├── docker/
│   └── compose/               # Docker Compose files
│       ├── basic.yml          # Basic services
│       └── advanced.yml       # Advanced services
├── monitoring/                # Monitoring configurations
│   ├── grafana/              # Grafana dashboards
│   └── prometheus/           # Prometheus configs
└── test_results/             # Test results and outputs
```

## 🧪 Testing Framework

The lab includes a comprehensive testing framework that:

### Agent Testing
- Tests Terraform agent with various requirements
- Validates generated code syntax and structure
- Measures response time and confidence
- Saves test results for analysis

### Infrastructure Validation
- Validates Terraform configurations
- Tests Docker Compose deployments
- Checks service connectivity
- Validates security configurations

### Performance Testing
- Measures agent response times
- Tests with different complexity levels
- Validates cost estimates
- Checks resource optimization

## 🔧 Prerequisites

### Required Tools
- **Terraform** (>= 1.0)
- **Docker** and **Docker Compose**
- **AWS CLI** (for real deployments)
- **Python 3.8+**

### AWS Setup (for real deployments)
```bash
# Configure AWS credentials
aws configure

# Set default region
export AWS_DEFAULT_REGION=us-east-1
```

## 📊 Test Scenarios

### 1. Basic Web Application
```json
{
  "project_name": "Basic Web App",
  "cloud_provider": "AWS",
  "user_load": "100",
  "budget": "50",
  "security": "basic"
}
```

### 2. High Traffic Application
```json
{
  "project_name": "High Traffic App",
  "cloud_provider": "AWS",
  "user_load": "10000",
  "budget": "500",
  "security": "high",
  "uptime": "99.9%"
}
```

### 3. Microservices Architecture
```json
{
  "project_name": "Microservices App",
  "cloud_provider": "AWS",
  "user_load": "5000",
  "budget": "300",
  "security": "high",
  "monitoring": "all",
  "architecture": "microservices"
}
```

## 🎯 Lab Workflow

### 1. **Development Phase**
- Use Docker Compose for local testing
- Test agent responses without AWS costs
- Validate Terraform syntax and structure

### 2. **Validation Phase**
- Deploy to AWS with dry-run first
- Test actual infrastructure deployment
- Validate agent-generated configurations

### 3. **Production Phase**
- Deploy production-like environments
- Test monitoring and alerting
- Validate security configurations

## 🔍 Monitoring and Observability

The lab includes monitoring setup for:

- **Prometheus** for metrics collection
- **Grafana** for visualization
- **Application logs** for debugging
- **Infrastructure metrics** for optimization

## 🛡️ Security Testing

The lab validates:

- **Security groups** and network ACLs
- **IAM roles** and policies
- **Encryption** at rest and in transit
- **Compliance** with best practices

## 📈 Performance Testing

The lab measures:

- **Agent response times**
- **Infrastructure deployment speed**
- **Resource utilization**
- **Cost optimization**

## 🧹 Cleanup and Maintenance

### Automatic Cleanup
```bash
# Clean up all resources
python lab/run_lab.py cleanup --environment basic
```

### Manual Cleanup
```bash
# Remove Docker containers
docker-compose -f lab/docker/compose/basic.yml down

# Remove Terraform state
rm -rf lab/terraform/environments/*/.terraform
```

## 🐛 Troubleshooting

### Common Issues

1. **Terraform Init Fails**
   - Check AWS credentials
   - Verify region configuration
   - Ensure Terraform version compatibility

2. **Docker Compose Issues**
   - Check Docker daemon status
   - Verify port availability
   - Check resource limits

3. **Agent Test Failures**
   - Check Python dependencies
   - Verify model availability
   - Check file permissions

### Debug Mode
```bash
# Enable debug logging
export TF_LOG=DEBUG
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run with verbose output
python lab/test_agents.py --verbose
```

## 📚 Additional Resources

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [AWS Best Practices](https://aws.amazon.com/architecture/well-architected/)

## 🤝 Contributing

To add new test scenarios or environments:

1. Create new environment in `terraform/environments/`
2. Add test case to `test_agents.py`
3. Update documentation
4. Test thoroughly before submitting

## 📄 License

This lab setup is part of the AI-AH project and follows the same license terms.

