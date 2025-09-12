# AI-AH Multi-Agent Infrastructure Platform

A comprehensive AI-powered platform for infrastructure automation, management, and optimization.

## Features

- **Multi-Agent Architecture**: Specialized agents for Terraform, Ansible, Kubernetes, Security, and Monitoring
- **Intelligent Reasoning**: AI-driven decision making and response generation
- **Local Training Lab**: Complete local environment for agent development and testing
- **Production Ready**: Scalable, secure, and compliant infrastructure management
- **S3-Compatible Storage**: MinIO integration for cost-effective object storage

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI-AH PLATFORM                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Terraform  │  │   Ansible   │  │ Kubernetes  │        │
│  │    Agent    │  │    Agent    │  │    Agent    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Security   │  │ Monitoring  │  │   Core      │        │
│  │    Agent    │  │    Agent    │  │ Framework   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Local Training Lab

The platform includes a comprehensive local training lab for agent development:

- **MinIO**: S3-compatible object storage
- **Prometheus + Grafana**: Monitoring and observability
- **ELK Stack**: Log aggregation and analysis
- **Vault**: Secrets management
- **Jenkins**: CI/CD pipeline

### Quick Start

```bash
# Setup the training lab
cd lab
python setup_lab.py

# Access services
# MinIO Console: http://localhost:9001
# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090
```

## Project Structure

```
AI-AH/
├── ai_ah_platform/          # Core platform code
│   ├── agents/              # Agent implementations
│   ├── core/                # Core framework
│   ├── api/                 # API layer
│   ├── tools/               # Tool integrations
│   └── ui/                  # User interfaces
├── lab/                     # Training lab environment
├── tests/                   # Test files
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
└── config/                  # Configuration files
```

## Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- 16GB+ RAM (for lab)
- 50GB+ disk space (for lab)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd AI-AH

# Install dependencies
pip install -r requirements.txt

# Setup training lab
cd lab
python setup_lab.py
```

### Running the Platform

```bash
# Start the platform
python main.py

# Access web interface
open http://localhost:8000
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/e2e/
```

## Documentation

- [Architecture Documentation](docs/architecture/)
- [Deployment Guide](docs/deployment/)
- [User Guides](docs/user-guides/)
- [API Documentation](docs/api/)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test in the lab environment
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the training lab examples
