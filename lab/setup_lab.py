#!/usr/bin/env python3
"""
Local Training Lab Setup Script
AI-AH Multi-Agent Infrastructure Platform

This script sets up a comprehensive local training lab for agent development and testing.
"""

import os
import sys
import subprocess
import time
import json
import requests
from pathlib import Path
from typing import Dict, List, Any
import yaml

class LabSetup:
    def __init__(self):
        self.lab_dir = Path(__file__).parent
        self.config_dir = self.lab_dir / "configs"
        self.data_dir = self.lab_dir / "data"
        self.logs_dir = self.lab_dir / "logs"
        
        # Service endpoints
        self.services = {
            "minio": {"url": "http://localhost:9000", "console": "http://localhost:9001"},
            "prometheus": {"url": "http://localhost:9090"},
            "grafana": {"url": "http://localhost:3000"},
            "nginx": {"url": "http://localhost:80"}
        }
        
        # MinIO configuration
        self.minio_config = {
            "access_key": "minioadmin",
            "secret_key": "minioadmin123",
            "buckets": [
                "terraform-state",
                "ansible-artifacts", 
                "kubernetes-backups",
                "security-reports",
                "monitoring-data",
                "ai-training-data"
            ]
        }

    def create_directories(self):
        """Create necessary directories for the lab."""
        print("📁 Creating lab directories...")
        
        directories = [
            self.config_dir,
            self.data_dir,
            self.logs_dir,
            self.config_dir / "prometheus",
            self.config_dir / "grafana" / "dashboards",
            self.config_dir / "grafana" / "datasources",
            self.config_dir / "logstash" / "pipeline",
            self.config_dir / "nginx"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {directory}")

    def create_config_files(self):
        """Create configuration files for all services."""
        print("⚙️ Creating configuration files...")
        
        # Prometheus configuration
        self.create_prometheus_config()
        
        # Grafana configuration
        self.create_grafana_config()
        
        # Logstash configuration
        self.create_logstash_config()
        
        # Nginx configuration
        self.create_nginx_config()

    def create_prometheus_config(self):
        """Create Prometheus configuration."""
        prometheus_config = {
            "global": {
                "scrape_interval": "15s",
                "evaluation_interval": "15s"
            },
            "rule_files": [],
            "scrape_configs": [
                {
                    "job_name": "prometheus",
                    "static_configs": [{"targets": ["localhost:9090"]}]
                },
                {
                    "job_name": "minio",
                    "static_configs": [{"targets": ["minio:9000"]}]
                },
                {
                    "job_name": "node-exporter",
                    "static_configs": [{"targets": ["node-exporter:9100"]}]
                }
            ]
        }
        
        config_file = self.config_dir / "prometheus.yml"
        with open(config_file, 'w') as f:
            yaml.dump(prometheus_config, f, default_flow_style=False)
        print(f"  ✅ Created: {config_file}")

    def create_grafana_config(self):
        """Create Grafana configuration."""
        # Datasource configuration
        datasource_config = {
            "apiVersion": 1,
            "datasources": [
                {
                    "name": "Prometheus",
                    "type": "prometheus",
                    "url": "http://prometheus:9090",
                    "access": "proxy",
                    "isDefault": True
                }
            ]
        }
        
        datasource_file = self.config_dir / "grafana" / "datasources" / "prometheus.yml"
        with open(datasource_file, 'w') as f:
            yaml.dump(datasource_config, f, default_flow_style=False)
        print(f"  ✅ Created: {datasource_file}")

    def create_logstash_config(self):
        """Create Logstash configuration."""
        logstash_config = """
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][service] == "minio" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{WORD:level} %{GREEDYDATA:message}" }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "lab-logs-%{+YYYY.MM.dd}"
  }
}
"""
        
        config_file = self.config_dir / "logstash" / "pipeline" / "logstash.conf"
        with open(config_file, 'w') as f:
            f.write(logstash_config)
        print(f"  ✅ Created: {config_file}")

    def create_nginx_config(self):
        """Create Nginx configuration."""
        nginx_config = """
events {
    worker_connections 1024;
}

http {
    upstream minio {
        server minio:9000;
    }
    
    upstream prometheus {
        server prometheus:9090;
    }
    
    upstream grafana {
        server grafana:3000;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        location /minio/ {
            proxy_pass http://minio/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /prometheus/ {
            proxy_pass http://prometheus/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /grafana/ {
            proxy_pass http://grafana/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
"""
        
        config_file = self.config_dir / "nginx" / "nginx.conf"
        with open(config_file, 'w') as f:
            f.write(nginx_config)
        print(f"  ✅ Created: {config_file}")

    def check_docker(self):
        """Check if Docker is installed and running."""
        print("🐳 Checking Docker installation...")
        
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ Docker installed: {result.stdout.strip()}")
            else:
                print("  ❌ Docker not found. Please install Docker first.")
                return False
        except FileNotFoundError:
            print("  ❌ Docker not found. Please install Docker first.")
            return False
        
        try:
            result = subprocess.run(["docker", "info"], capture_output=True, text=True)
            if result.returncode == 0:
                print("  ✅ Docker daemon is running")
                return True
            else:
                print("  ❌ Docker daemon is not running. Please start Docker.")
                return False
        except Exception as e:
            print(f"  ❌ Error checking Docker daemon: {e}")
            return False

    def start_services(self):
        """Start all lab services using Docker Compose."""
        print("🚀 Starting lab services...")
        
        os.chdir(self.lab_dir)
        
        try:
            # Start services with simplified compose file first
            result = subprocess.run(
                ["docker-compose", "-f", "docker-compose-simple.yml", "up", "-d"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("  ✅ Services started successfully")
                return True
            else:
                print(f"  ❌ Error starting services: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error starting services: {e}")
            return False

    def wait_for_services(self):
        """Wait for services to be ready."""
        print("⏳ Waiting for services to be ready...")
        
        for service, config in self.services.items():
            if service == "minio":
                # Check MinIO API
                self.wait_for_service(service, config["url"], timeout=60)
            elif service == "prometheus":
                self.wait_for_service(service, config["url"], timeout=60)
            elif service == "grafana":
                self.wait_for_service(service, config["url"], timeout=60)

    def wait_for_service(self, service_name: str, url: str, timeout: int = 30):
        """Wait for a specific service to be ready."""
        print(f"  🔍 Checking {service_name}...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code in [200, 401, 403]:  # 401/403 means service is up but needs auth
                    print(f"    ✅ {service_name} is ready")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(2)
        
        print(f"    ⚠️ {service_name} not ready after {timeout}s")
        return False

    def setup_minio_buckets(self):
        """Setup MinIO buckets for agent training."""
        print("🗄️ Setting up MinIO buckets...")
        
        # Install MinIO client
        try:
            subprocess.run(["docker", "run", "--rm", "-v", f"{self.lab_dir}:/data", 
                          "minio/mc", "alias", "set", "local", "http://minio:9000", 
                          self.minio_config["access_key"], self.minio_config["secret_key"]], 
                         check=True)
        except subprocess.CalledProcessError:
            print("  ⚠️ Could not setup MinIO client")
            return
        
        # Create buckets
        for bucket in self.minio_config["buckets"]:
            try:
                subprocess.run(["docker", "run", "--rm", "--network", "lab_lab-network",
                              "minio/mc", "mb", f"local/{bucket}"], check=True)
                print(f"  ✅ Created bucket: {bucket}")
            except subprocess.CalledProcessError:
                print(f"  ⚠️ Could not create bucket: {bucket}")

    def create_agent_test_scenarios(self):
        """Create test scenarios for agent training."""
        print("🧪 Creating agent test scenarios...")
        
        scenarios = {
            "terraform": {
                "name": "Terraform S3 Bucket Creation",
                "description": "Create S3 bucket using MinIO for state storage",
                "steps": [
                    "Initialize Terraform with MinIO backend",
                    "Create S3 bucket resource",
                    "Apply configuration",
                    "Validate bucket creation"
                ]
            },
            "ansible": {
                "name": "Ansible Configuration Management",
                "description": "Deploy web server and configure with Ansible",
                "steps": [
                    "Create inventory file",
                    "Write playbook for web server setup",
                    "Execute playbook",
                    "Verify configuration"
                ]
            },
            "kubernetes": {
                "name": "Kubernetes Application Deployment",
                "description": "Deploy application to Kubernetes cluster",
                "steps": [
                    "Create deployment manifest",
                    "Create service manifest",
                    "Apply to cluster",
                    "Verify deployment"
                ]
            },
            "security": {
                "name": "Security Vulnerability Scanning",
                "description": "Scan infrastructure for vulnerabilities",
                "steps": [
                    "Run Trivy vulnerability scan",
                    "Generate security report",
                    "Store results in MinIO",
                    "Create compliance dashboard"
                ]
            },
            "monitoring": {
                "name": "Monitoring Stack Setup",
                "description": "Setup monitoring and alerting",
                "steps": [
                    "Configure Prometheus targets",
                    "Create Grafana dashboards",
                    "Setup alerting rules",
                    "Verify monitoring data"
                ]
            }
        }
        
        scenarios_file = self.data_dir / "test_scenarios.json"
        with open(scenarios_file, 'w') as f:
            json.dump(scenarios, f, indent=2)
        print(f"  ✅ Created: {scenarios_file}")

    def print_lab_info(self):
        """Print lab information and access details."""
        print("\n" + "="*60)
        print("🎉 LOCAL TRAINING LAB SETUP COMPLETE!")
        print("="*60)
        
        print("\n📊 Service Access URLs:")
        for service, config in self.services.items():
            if service == "minio":
                print(f"  🗄️ MinIO Console: {config['console']} (admin/minioadmin123)")
                print(f"  🗄️ MinIO API: {config['url']}")
            else:
                print(f"  🔗 {service.title()}: {config['url']}")
        
        print("\n🔑 Default Credentials:")
        print("  MinIO: minioadmin / minioadmin123")
        print("  Grafana: admin / admin123")
        print("  Vault: root (dev mode)")
        
        print("\n📁 Lab Structure:")
        print(f"  Config: {self.config_dir}")
        print(f"  Data: {self.data_dir}")
        print(f"  Logs: {self.logs_dir}")
        
        print("\n🚀 Next Steps:")
        print("  1. Test agent integrations with MinIO")
        print("  2. Run training scenarios")
        print("  3. Validate agent capabilities")
        print("  4. Monitor performance and logs")
        
        print("\n🛑 To stop the lab:")
        print("  docker-compose down")

    def run(self):
        """Run the complete lab setup."""
        print("🧪 AI-AH Local Training Lab Setup")
        print("="*50)
        
        # Check prerequisites
        if not self.check_docker():
            return False
        
        # Setup lab
        self.create_directories()
        self.create_config_files()
        
        # Start services
        if not self.start_services():
            return False
        
        # Wait for services
        self.wait_for_services()
        
        # Setup MinIO
        self.setup_minio_buckets()
        
        # Create test scenarios
        self.create_agent_test_scenarios()
        
        # Print lab info
        self.print_lab_info()
        
        return True

if __name__ == "__main__":
    lab = LabSetup()
    success = lab.run()
    
    if success:
        print("\n✅ Lab setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Lab setup failed!")
        sys.exit(1)
