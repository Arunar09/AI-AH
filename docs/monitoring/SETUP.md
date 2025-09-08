# 📊 Monitoring Setup Guide

This document explains the monitoring infrastructure for the AI-AH project, including how to set it up, use it, and extend it.

## Table of Contents
1. [Overview](#-overview)
2. [Components](#-components)
3. [Setup Instructions](#-setup-instructions)
4. [Usage Guide](#-usage-guide)
5. [Troubleshooting](#-troubleshooting)
6. [Extending the System](#-extending-the-system)

## 🌟 Overview

The monitoring system provides real-time insights into the health and quality of the AI-AH project. It consists of:

- **Project Health Monitor**: Collects metrics about documentation, tests, and code quality
- **Dashboard**: Visualizes metrics in an interactive web interface
- **CI/CD Integration**: Automatically runs checks on every commit
- **Alerts**: Notifies about critical issues

## 🧩 Components

### 1. Project Health Monitor (`scripts/monitor_health.py`)
- Collects metrics from various sources
- Generates JSON reports in `metrics/project_health.json`
- Can be run manually or as part of CI/CD

### 2. Dashboard (`dashboard/`)
- Interactive web interface
- Real-time metrics visualization
- Historical trends

### 3. CI/CD Integration (`.github/workflows/ci.yml`)
- Runs health checks on every push/PR
- Enforces quality gates
- Generates reports

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 16+ (for dashboard development)
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/ai-ah.git
   cd ai-ah
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

3. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

4. **Run the health monitor**
   ```bash
   python scripts/monitor_health.py
   ```

5. **View the dashboard**
   ```bash
   # Using Python's built-in server
   python -m http.server 8000
   ```
   Then open http://localhost:8000/dashboard in your browser

## 🚀 Usage Guide

### Running Health Checks

#### Manual Run
```bash
python scripts/monitor_health.py
```

#### Scheduled Runs (cron)
Add to crontab to run hourly:
```
0 * * * * cd /path/to/ai-ah && ./venv/bin/python scripts/monitor_health.py
```

### Interpreting the Dashboard

#### Key Metrics
- **Documentation Coverage**: Ratio of documented to undocumented code
- **Test Coverage**: Percentage of code covered by tests
- **Code Quality**: Number of code quality issues found

#### Status Indicators
- 🟢 Healthy: Above 80%
- 🟡 Warning: 50-80%
- 🔴 Critical: Below 50%

### CI/CD Integration
The CI/CD pipeline automatically:
1. Runs tests and collects coverage
2. Validates documentation
3. Checks code quality
4. Generates reports

## 🐛 Troubleshooting

### Common Issues

#### Dashboard Not Updating
1. Ensure the health monitor is running
2. Check browser console for errors
3. Verify CORS settings if accessing from a different domain

#### Missing Metrics
1. Check if all required tools are installed
2. Verify file permissions
3. Look for errors in the console output

### Logs
Check these locations for troubleshooting:
- CI/CD: GitHub Actions logs
- Health Monitor: Console output or system logs
- Dashboard: Browser developer console

## 🔧 Extending the System

### Adding New Metrics
1. Edit `scripts/monitor_health.py`
2. Add your metric collection function
3. Update the dashboard to display the new metric

### Customizing the Dashboard
1. Edit files in `dashboard/`
2. Add new charts using Chart.js
3. Update the styling in `index.html`

### Adding Alerts
1. Modify the health monitor to check thresholds
2. Add notification logic (email, Slack, etc.)
3. Update the dashboard to show alert status

## 📈 Best Practices

1. **Regular Maintenance**
   - Update dependencies regularly
   - Review and update thresholds
   - Archive old metrics

2. **Performance**
   - Run intensive tasks asynchronously
   - Cache results when possible
   - Optimize database queries

3. **Security**
   - Never expose sensitive data in metrics
   - Use authentication for the dashboard
   - Keep dependencies updated

## 📚 Related Documents

- [Project Governance](../PROJECT_GOVERNANCE.md)
- [CI/CD Configuration](../.github/workflows/ci.yml)
- [Development Setup](../docs/onboarding/CONTRIBUTING.md)
