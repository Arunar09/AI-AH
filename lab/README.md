# 🧪 AI-AH Local Training Lab

A comprehensive local training environment for AI-AH Multi-Agent Infrastructure Platform agents.

## 🎯 **Overview**

This lab provides a complete local environment for training and validating our infrastructure agents using [MinIO](https://www.min.io/) as the primary object storage solution. MinIO's S3-compatible API makes it perfect for training agents to work with cloud storage without the cost and complexity of real cloud providers.

## 🏗️ **Lab Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    LOCAL TRAINING LAB                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   MinIO     │  │ Prometheus  │  │   Grafana   │        │
│  │ S3 Storage  │  │  Metrics    │  │ Dashboards  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ ELK Stack   │  │   Vault     │  │   Jenkins   │        │
│  │   Logging   │  │   Secrets   │  │    CI/CD    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ SonarQube   │  │    Trivy    │  │    Nginx    │        │
│  │ Code Quality│  │  Security   │  │ Load Balancer│       │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 **Quick Start**

### **Prerequisites**
- Docker and Docker Compose
- Python 3.8+
- 16GB+ RAM recommended
- 50GB+ disk space

### **Setup Lab**
```bash
# Clone and navigate to lab directory
cd lab

# Run the setup script
python setup_lab.py

# Or manually start services
docker-compose up -d
```

### **Access Services**
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin123)
- **MinIO API**: http://localhost:9000
- **Grafana**: http://localhost:3000 (admin/admin123)
- **Prometheus**: http://localhost:9090
- **Kibana**: http://localhost:5601
- **Vault**: http://localhost:8200 (root token)
- **Jenkins**: http://localhost:8080

## 🗄️ **MinIO Integration**

### **Why MinIO?**
Based on [MinIO's capabilities](https://www.min.io/):
- **S3-Compatible API**: Perfect for AWS S3 training
- **AI Data Storage**: Built for AI workloads with exascale performance
- **Local Deployment**: Runs anywhere without cloud dependencies
- **Cost Effective**: 40% lower TCO compared to cloud storage
- **High Performance**: 21.8TiB/s throughput at exabyte scale

### **Pre-configured Buckets**
- `terraform-state`: Terraform remote state storage
- `ansible-artifacts`: Ansible playbook artifacts and logs
- `kubernetes-backups`: Kubernetes cluster backups
- `security-reports`: Security scan reports and compliance data
- `monitoring-data`: Monitoring metrics and logs
- `ai-training-data`: AI model training data and artifacts

## 🔧 **Agent Training Scenarios**

### **1. Terraform Agent**
```bash
cd terraform
terraform init
terraform plan
terraform apply
```
**Training Focus**: S3 bucket creation, state management, resource provisioning

### **2. Ansible Agent**
```bash
cd ansible
ansible-playbook -i inventory playbooks/minio-setup.yml
```
**Training Focus**: Configuration management, automation, service setup

### **3. Kubernetes Agent**
```bash
kubectl apply -f kubernetes/minio-storage.yaml
```
**Training Focus**: Storage classes, persistent volumes, backup automation

### **4. Security Agent**
```bash
# Run vulnerability scans
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image minio/minio:latest

# Store results in MinIO
mc cp scan-results.json local/security-reports/
```
**Training Focus**: Vulnerability scanning, compliance validation, security monitoring

### **5. Monitoring Agent**
```bash
# Configure Prometheus to scrape MinIO metrics
# Create Grafana dashboards for MinIO monitoring
# Setup alerting rules for storage usage
```
**Training Focus**: Metrics collection, dashboard creation, alerting configuration

## 📊 **Training Scenarios**

### **Scenario 1: Web Application with Object Storage**
```yaml
Components:
  - Load balancer (Nginx)
  - Web servers (2x instances)
  - Database (PostgreSQL)
  - Object storage (MinIO)
  - Monitoring (Prometheus/Grafana)

Agents Involved:
  - Terraform: Infrastructure provisioning
  - Ansible: Configuration management
  - Kubernetes: Application deployment
  - Security: Security scanning
  - Monitoring: Observability setup
```

### **Scenario 2: AI Data Pipeline**
```yaml
Components:
  - Data ingestion (Kafka)
  - Processing (Spark)
  - Storage (MinIO)
  - Analytics (Jupyter)
  - Monitoring (ELK Stack)

Agents Involved:
  - Terraform: Infrastructure setup
  - Ansible: Service configuration
  - Kubernetes: Container orchestration
  - Security: Data protection
  - Monitoring: Pipeline monitoring
```

### **Scenario 3: Multi-Environment Deployment**
```yaml
Environments:
  - Development: Single instance
  - Staging: Load balanced
  - Production: High availability

Agents Involved:
  - Terraform: Environment-specific configs
  - Ansible: Environment-specific playbooks
  - Kubernetes: Namespace isolation
  - Security: Compliance validation
  - Monitoring: Environment monitoring
```

## 🛠️ **Lab Management**

### **Start Lab**
```bash
docker-compose up -d
```

### **Stop Lab**
```bash
docker-compose down
```

### **View Logs**
```bash
docker-compose logs -f [service-name]
```

### **Reset Lab**
```bash
docker-compose down -v
docker system prune -a
python setup_lab.py
```

### **Backup Lab Data**
```bash
# Backup MinIO data
docker run --rm -v minio_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/minio-backup.tar.gz -C /data .

# Backup configuration
tar czf lab-config-backup.tar.gz configs/
```

## 📈 **Performance Monitoring**

### **Resource Usage**
```bash
# Check container resource usage
docker stats

# Check disk usage
docker system df

# Check network usage
docker network ls
```

### **Service Health**
```bash
# Check service health
curl http://localhost:9000/minio/health/live
curl http://localhost:9090/-/healthy
curl http://localhost:3000/api/health
```

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Services not starting**
   ```bash
   # Check Docker daemon
   docker info
   
   # Check port conflicts
   netstat -tulpn | grep :9000
   ```

2. **MinIO connection issues**
   ```bash
   # Check MinIO logs
   docker-compose logs minio
   
   # Test MinIO connectivity
   curl http://localhost:9000/minio/health/live
   ```

3. **High resource usage**
   ```bash
   # Check resource usage
   docker stats
   
   # Adjust resource limits in docker-compose.yml
   ```

### **Log Locations**
- **MinIO**: `docker-compose logs minio`
- **Prometheus**: `docker-compose logs prometheus`
- **Grafana**: `docker-compose logs grafana`
- **All services**: `docker-compose logs`

## 📚 **Documentation**

- [MinIO Documentation](https://docs.min.io/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test in the lab environment
5. Submit a pull request

## 📄 **License**

This lab is part of the AI-AH Multi-Agent Infrastructure Platform project.

---

**Status: 🚀 READY FOR AGENT TRAINING**
