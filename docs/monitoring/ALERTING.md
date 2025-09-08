# 🚨 Alerting System Guide

This document explains how to configure and use the AI-AH alerting system to monitor your infrastructure and receive notifications about critical issues.

## Table of Contents
1. [Overview](#-overview)
2. [Alert Types](#-alert-types)
3. [Configuration](#-configuration)
4. [Setting Up Notifications](#-setting-up-notifications)
5. [Testing Alerts](#-testing-alerts)
6. [Custom Alerts](#-custom-alerts)
7. [Troubleshooting](#-troubleshooting)

## 🌟 Overview

The alerting system monitors your infrastructure and sends notifications when issues are detected. It integrates with:

- Email (SMTP)
- Slack
- Webhooks (coming soon)

## 🚨 Alert Types

### 1. Security Alerts
- Critical security findings
- High priority vulnerabilities
- Compliance violations

### 2. Cost Alerts
- Unexpected cost increases
- Budget threshold reached
- Unusual spending patterns

### 3. Infrastructure Alerts
- Unmanaged resources
- Drift detection
- Configuration errors

## ⚙️ Configuration

Alerting is configured in `config/alerts.json`:

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "username": "your-email@example.com",
    "password": "your-password",
    "from_addr": "alerts@ai-ah.example.com",
    "to_addrs": ["admin@example.com"]
  },
  "slack": {
    "enabled": false,
    "webhook_url": "https://hooks.slack.com/services/...",
    "channel": "#alerts"
  },
  "thresholds": {
    "critical_security_findings": 1,
    "high_security_findings": 3,
    "cost_increase_percent": 20,
    "unmanaged_resources": 1
  }
}
```

## 📧 Setting Up Email Notifications

1. Enable email in `alerts.json`:
   ```json
   "email": {
     "enabled": true,
     "smtp_server": "smtp.gmail.com",
     "smtp_port": 587,
     "username": "your-email@gmail.com",
     "password": "your-app-password",
     "from_addr": "alerts@ai-ah.example.com",
     "to_addrs": ["admin@example.com"]
   }
   ```

2. For Gmail, you'll need an [App Password](https://myaccount.google.com/apppasswords)

## 💬 Setting Up Slack Notifications

1. Create an [Incoming Webhook](https://api.slack.com/messaging/webhooks)
2. Enable Slack in `alerts.json`:
   ```json
   "slack": {
     "enabled": true,
     "webhook_url": "https://hooks.slack.com/services/...",
     "channel": "#alerts"
   }
   ```

## 🧪 Testing Alerts

Run the alerting system manually:

```bash
python scripts/alerting.py
```

Or trigger a test alert:

```python
from scripts.alerting import AlertManager

alert = {
    'severity': 'critical',
    'title': 'Test Alert',
    'message': 'This is a test of the alerting system',
    'timestamp': '2023-01-01T00:00:00Z'
}

manager = AlertManager()
manager.send_alert(alert)
```

## 🛠️ Custom Alerts

To add a new alert type:

1. Add a new condition in `scripts/alerting.py` `check_metrics()`
2. Update the thresholds in `config/alerts.json`
3. Add any necessary metrics collection

Example:

```python
# In check_metrics()
if some_condition:
    alerts.append({
        'severity': 'high',
        'title': 'Custom Alert',
        'message': 'Description of the issue',
        'timestamp': datetime.utcnow().isoformat()
    })
```

## 🐛 Troubleshooting

### Common Issues

1. **Emails not sending**
   - Check SMTP settings and credentials
   - Verify port is not blocked
   - Check spam folder

2. **Slack notifications not working**
   - Verify webhook URL is correct
   - Check channel exists and bot has access
   - Check Slack's rate limits

3. **No alerts being generated**
   - Verify metrics are being collected
   - Check threshold values
   - Look for errors in logs

### Logs

Check these locations for error messages:
- CI/CD pipeline logs
- Application logs
- Email/Slack delivery logs

## 📈 Monitoring Alert History

Alert history is stored in `logs/alerts.log` with timestamps and details.

## 🔄 Automation

For production, set up a scheduled task to run the alerting system regularly:

```bash
# Run every 15 minutes
*/15 * * * * cd /path/to/ai-ah && ./venv/bin/python scripts/alerting.py
```

## 🔒 Security Considerations

- Never commit sensitive credentials to version control
- Use environment variables for production secrets
- Restrict access to alerting configuration
- Regularly rotate API keys and passwords

## 📚 Related Documents

- [Monitoring Setup](./SETUP.md)
- [CI/CD Pipeline](../.github/workflows/ci.yml)
- [Security Guidelines](../SECURITY.md)
