#!/usr/bin/env python3
"""
Repository Cleanup Script
AI-AH Multi-Agent Infrastructure Platform

This script cleans and organizes the repository structure.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any
import json

class RepositoryCleanup:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.backup_dir = self.repo_root / "backup_pre_cleanup"
        
        # Files to remove
        self.files_to_remove = [
            # Test files in root
            "test_agent_intelligence.py",
            "test_agent_interaction.py", 
            "test_chat_interactive.py",
            "test_cli_demo.py",
            "test_complex_queries.py",
            "test_context_awareness_learning.py",
            "test_enhanced_agent_direct.py",
            "test_enhanced_agent_integration.py",
            "test_error_handling.py",
            "test_final_fixes.py",
            "test_framework_enhancements.py",
            "test_intelligent_behavior.py",
            "test_pattern_matching.py",
            "test_platform.py",
            "test_real_data_flow.py",
            "test_reasoning_engine.py",
            "test_reasoning.py",
            "test_server_response.py",
            "test_simple_enhancements.py",
            "test_ui_fixes.py",
            
            # Demo files
            "demo_ai_agent_behavior.py",
            "demo_enhanced_agent.py",
            "demo_real_time.py",
            
            # Analysis files
            "analyze_generic_responses.py",
            "enhanced_knowledge_base_methods.py",
            "intelligence_test_suite.py",
            "interactive_agent_training.py",
            "interactive_test.py",
            "reasoning_analysis_demo.py",
            "scaling_test_agent.py",
            
            # Duplicate documentation
            "AGENT_TRAINING_LAB_PLAN.md",
            "COMPREHENSIVE_TEST_REPORT.md",
            "REASONING_ENGINE_ENHANCEMENT_REPORT.md",
            "REASONING_ENGINE_IMPLEMENTATION_REPORT.md",
            "ISSUES_AND_FIXES.md",
            "MULTI_AGENT_INFRASTRUCTURE_PLATFORM_PLAN.md",
            "PROJECT_DEVELOPER_GUIDE.md",
            "CONTEXT.md"
        ]
        
        # Directories to remove
        self.dirs_to_remove = [
            "local-dev"  # Duplicate of lab/
        ]
        
        # Files to move
        self.files_to_move = {
            "PRODUCTION_READINESS_ASSESSMENT.md": "docs/architecture/",
            "LOCAL_TRAINING_LAB_DESIGN.md": "docs/architecture/",
            "REPOSITORY_CLEANUP_PLAN.md": "docs/architecture/"
        }

    def create_backup(self):
        """Create backup of current repository state."""
        print("💾 Creating backup...")
        
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        
        self.backup_dir.mkdir(exist_ok=True)
        
        # Backup important files
        important_files = [
            "README.md",
            "requirements.txt",
            "main.py",
            "pytest.ini"
        ]
        
        for file in important_files:
            src = self.repo_root / file
            if src.exists():
                shutil.copy2(src, self.backup_dir / file)
        
        print(f"  ✅ Backup created at: {self.backup_dir}")

    def create_directories(self):
        """Create necessary directory structure."""
        print("📁 Creating directory structure...")
        
        directories = [
            "tests/unit",
            "tests/integration", 
            "tests/e2e",
            "tests/fixtures",
            "docs/architecture",
            "docs/deployment",
            "docs/user-guides",
            "docs/api",
            "scripts/setup",
            "scripts/maintenance",
            "scripts/deployment",
            ".github/workflows"
        ]
        
        for directory in directories:
            dir_path = self.repo_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {directory}")

    def remove_files(self):
        """Remove unnecessary files."""
        print("🗑️ Removing unnecessary files...")
        
        removed_count = 0
        for file in self.files_to_remove:
            file_path = self.repo_root / file
            if file_path.exists():
                file_path.unlink()
                print(f"  ✅ Removed: {file}")
                removed_count += 1
            else:
                print(f"  ⚠️ Not found: {file}")
        
        print(f"  📊 Removed {removed_count} files")

    def remove_directories(self):
        """Remove unnecessary directories."""
        print("🗑️ Removing unnecessary directories...")
        
        removed_count = 0
        for directory in self.dirs_to_remove:
            dir_path = self.repo_root / directory
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"  ✅ Removed: {directory}")
                removed_count += 1
            else:
                print(f"  ⚠️ Not found: {directory}")
        
        print(f"  📊 Removed {removed_count} directories")

    def move_files(self):
        """Move files to appropriate locations."""
        print("📦 Moving files to appropriate locations...")
        
        moved_count = 0
        for file, destination in self.files_to_move.items():
            src = self.repo_root / file
            dst_dir = self.repo_root / destination
            dst = dst_dir / file
            
            if src.exists():
                # Ensure destination directory exists
                dst_dir.mkdir(parents=True, exist_ok=True)
                
                # Move file
                shutil.move(str(src), str(dst))
                print(f"  ✅ Moved: {file} → {destination}")
                moved_count += 1
            else:
                print(f"  ⚠️ Not found: {file}")
        
        print(f"  📊 Moved {moved_count} files")

    def organize_test_files(self):
        """Organize test files into proper structure."""
        print("🧪 Organizing test files...")
        
        # Move existing test files from tests/ to tests/unit/
        tests_dir = self.repo_root / "tests"
        unit_tests_dir = tests_dir / "unit"
        
        if tests_dir.exists():
            for test_file in tests_dir.glob("test_*.py"):
                if test_file.name != "__init__.py":
                    shutil.move(str(test_file), str(unit_tests_dir / test_file.name))
                    print(f"  ✅ Moved: {test_file.name} → tests/unit/")

    def create_gitignore(self):
        """Create comprehensive .gitignore file."""
        print("📝 Creating .gitignore...")
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Docker
.dockerignore

# Kubernetes
*.kubeconfig

# Terraform
*.tfstate
*.tfstate.*
.terraform/
.terraform.lock.hcl

# Ansible
*.retry

# MinIO
minio-data/

# Lab data
lab/data/
lab/logs/

# Backup
backup_pre_cleanup/

# Temporary files
tmp/
temp/
*.tmp
*.temp

# Test coverage
.coverage
htmlcov/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
"""
        
        gitignore_path = self.repo_root / ".gitignore"
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
        
        print(f"  ✅ Created: .gitignore")

    def create_documentation(self):
        """Create essential documentation files."""
        print("📚 Creating documentation...")
        
        # Create tests README
        tests_readme = """# Tests

This directory contains all test files for the AI-AH platform.

## Structure

- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for component interactions
- `e2e/` - End-to-end tests for complete workflows
- `fixtures/` - Test data and fixtures

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run unit tests only
python -m pytest tests/unit/

# Run with coverage
python -m pytest tests/ --cov=ai_ah_platform
```

## Test Guidelines

1. Use descriptive test names
2. Follow AAA pattern (Arrange, Act, Assert)
3. Mock external dependencies
4. Keep tests independent
5. Use fixtures for common setup
"""
        
        tests_readme_path = self.repo_root / "tests" / "README.md"
        with open(tests_readme_path, 'w', encoding='utf-8') as f:
            f.write(tests_readme)
        
        # Create architecture README
        arch_readme = """# Architecture Documentation

This directory contains architecture and design documentation for the AI-AH platform.

## Documents

- `PRODUCTION_READINESS_ASSESSMENT.md` - Production readiness analysis
- `LOCAL_TRAINING_LAB_DESIGN.md` - Local training lab design
- `REPOSITORY_CLEANUP_PLAN.md` - Repository cleanup plan

## Architecture Overview

The AI-AH platform is built with a modular, agent-based architecture:

- **Core Framework**: Base platform and agent framework
- **Agents**: Specialized agents for different infrastructure tasks
- **API Layer**: RESTful API and WebSocket communication
- **Tools**: Integration with external tools and services
- **UI**: Web and CLI interfaces

## Design Principles

1. **Modularity**: Each component is independently deployable
2. **Scalability**: Horizontal scaling capabilities
3. **Security**: Built-in security and compliance features
4. **Observability**: Comprehensive monitoring and logging
5. **Extensibility**: Easy to add new agents and capabilities
"""
        
        arch_readme_path = self.repo_root / "docs" / "architecture" / "README.md"
        with open(arch_readme_path, 'w', encoding='utf-8') as f:
            f.write(arch_readme)
        
        print("  ✅ Created documentation files")

    def update_main_readme(self):
        """Update the main README.md file."""
        print("📝 Updating main README...")
        
        readme_content = """# AI-AH Multi-Agent Infrastructure Platform

A comprehensive AI-powered platform for infrastructure automation, management, and optimization.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for Terraform, Ansible, Kubernetes, Security, and Monitoring
- **Intelligent Reasoning**: AI-driven decision making and response generation
- **Local Training Lab**: Complete local environment for agent development and testing
- **Production Ready**: Scalable, secure, and compliant infrastructure management
- **S3-Compatible Storage**: MinIO integration for cost-effective object storage

## 🏗️ Architecture

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

## 🧪 Local Training Lab

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

## 📁 Project Structure

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

## 🚀 Getting Started

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

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/e2e/
```

## 📚 Documentation

- [Architecture Documentation](docs/architecture/)
- [Deployment Guide](docs/deployment/)
- [User Guides](docs/user-guides/)
- [API Documentation](docs/api/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test in the lab environment
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the training lab examples
"""
        
        readme_path = self.repo_root / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("  ✅ Updated main README.md")

    def validate_structure(self):
        """Validate the cleaned repository structure."""
        print("✅ Validating repository structure...")
        
        # Check essential files exist
        essential_files = [
            "README.md",
            "requirements.txt",
            "main.py",
            ".gitignore",
            "ai_ah_platform/__init__.py",
            "lab/README.md",
            "tests/README.md"
        ]
        
        missing_files = []
        for file in essential_files:
            if not (self.repo_root / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"  ❌ Missing files: {missing_files}")
            return False
        
        # Check directory structure
        essential_dirs = [
            "ai_ah_platform",
            "lab",
            "tests",
            "docs",
            "scripts",
            "config"
        ]
        
        missing_dirs = []
        for directory in essential_dirs:
            if not (self.repo_root / directory).exists():
                missing_dirs.append(directory)
        
        if missing_dirs:
            print(f"  ❌ Missing directories: {missing_dirs}")
            return False
        
        print("  ✅ Repository structure is valid")
        return True

    def print_summary(self):
        """Print cleanup summary."""
        print("\n" + "="*60)
        print("🎉 REPOSITORY CLEANUP COMPLETE!")
        print("="*60)
        
        print("\n📊 Cleanup Summary:")
        print(f"  🗑️ Files removed: {len(self.files_to_remove)}")
        print(f"  🗑️ Directories removed: {len(self.dirs_to_remove)}")
        print(f"  📦 Files moved: {len(self.files_to_move)}")
        
        print("\n📁 New Structure:")
        print("  ✅ Clean root directory")
        print("  ✅ Organized test files")
        print("  ✅ Consolidated documentation")
        print("  ✅ Proper .gitignore")
        print("  ✅ Clear directory structure")
        
        print("\n🚀 Next Steps:")
        print("  1. Review the cleaned structure")
        print("  2. Test the platform functionality")
        print("  3. Setup the training lab")
        print("  4. Begin agent development")
        
        print("\n📚 Documentation:")
        print("  📖 Main README: README.md")
        print("  🧪 Lab Guide: lab/README.md")
        print("  🧪 Test Guide: tests/README.md")
        print("  🏗️ Architecture: docs/architecture/")

    def run(self):
        """Run the complete cleanup process."""
        print("🧹 AI-AH Repository Cleanup")
        print("="*50)
        
        try:
            # Create backup
            self.create_backup()
            
            # Create directories
            self.create_directories()
            
            # Remove files
            self.remove_files()
            
            # Remove directories
            self.remove_directories()
            
            # Move files
            self.move_files()
            
            # Organize test files
            self.organize_test_files()
            
            # Create .gitignore
            self.create_gitignore()
            
            # Create documentation
            self.create_documentation()
            
            # Update main README
            self.update_main_readme()
            
            # Validate structure
            if self.validate_structure():
                self.print_summary()
                return True
            else:
                print("❌ Repository structure validation failed")
                return False
                
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
            return False

if __name__ == "__main__":
    cleanup = RepositoryCleanup()
    success = cleanup.run()
    
    if success:
        print("\n✅ Repository cleanup completed successfully!")
        exit(0)
    else:
        print("\n❌ Repository cleanup failed!")
        exit(1)
