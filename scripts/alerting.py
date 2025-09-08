#!/usr/bin/env python3
"""
Infrastructure Alerting System

Monitors infrastructure metrics and sends alerts for critical issues.
"""
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests

class AlertManager:
    def __init__(self, config_path: str = 'config/alerts.json'):
        self.config = self._load_config(config_path)
        self.metrics_path = 'metrics/infra_metrics.json'
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load alerting configuration."""
        try:
            with open(config_path) as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'email': {
                    'enabled': False,
                    'smtp_server': 'smtp.example.com',
                    'smtp_port': 587,
                    'username': 'user@example.com',
                    'password': '',
                    'from_addr': 'alerts@ai-ah.example.com',
                    'to_addrs': ['admin@example.com']
                },
                'slack': {
                    'enabled': False,
                    'webhook_url': '',
                    'channel': '#alerts'
                },
                'thresholds': {
                    'critical_security_findings': 1,
                    'high_security_findings': 5,
                    'cost_increase_percent': 20,
                    'unmanaged_resources': 1
                }
            }
    
    def check_metrics(self) -> List[Dict[str, Any]]:
        """Check metrics against thresholds and return alerts."""
        alerts = []
        
        try:
            with open(self.metrics_path) as f:
                metrics = json.load(f)
            
            # Check security findings
            sec = metrics.get('infrastructure', {}).get('security', {})
            if 'scans' in sec:
                if sec['scans']['critical_findings'] >= self.config['thresholds']['critical_security_findings']:
                    alerts.append({
                        'severity': 'critical',
                        'title': 'Critical Security Finding',
                        'message': f"Found {sec['scans']['critical_findings']} critical security issues"
                    })
                
                if sec['scans']['high_findings'] >= self.config['thresholds']['high_security_findings']:
                    alerts.append({
                        'severity': 'high',
                        'title': 'High Priority Security Finding',
                        'message': f"Found {sec['scans']['high_findings']} high priority security issues"
                    })
            
            # Check cost anomalies
            cost = metrics.get('infrastructure', {}).get('cost', {})
            if 'monthly_estimate' in cost and 'previous_month' in cost:
                current = cost['monthly_estimate'].get('total', 0)
                previous = cost['previous_month'].get('total', 0)
                
                if previous > 0:  # Avoid division by zero
                    increase = ((current - previous) / previous) * 100
                    if increase >= self.config['thresholds']['cost_increase_percent']:
                        alerts.append({
                            'severity': 'high',
                            'title': 'Cost Increase Alert',
                            'message': f"Monthly cost increased by {increase:.1f}% (${current - previous:.2f})"
                        })
            
            # Check for unmanaged resources
            tf = metrics.get('infrastructure', {}).get('terraform', {})
            if 'unmanaged_resources' in tf and tf['unmanaged_resources'] > 0:
                alerts.append({
                    'severity': 'medium',
                    'title': 'Unmanaged Resources',
                    'message': f"Found {tf['unmanaged_resources']} resources not managed by Terraform"
                })
            
            return alerts
            
        except Exception as e:
            return [{
                'severity': 'critical',
                'title': 'Alerting System Error',
                'message': f"Failed to check metrics: {str(e)}"
            }]
    
    def send_alert(self, alert: Dict[str, Any]) -> bool:
        """Send an alert through all configured channels."""
        success = True
        
        if self.config.get('email', {}).get('enabled', False):
            success &= self._send_email_alert(alert)
        
        if self.config.get('slack', {}).get('enabled', False):
            success &= self._send_slack_alert(alert)
        
        return success
    
    def _send_email_alert(self, alert: Dict[str, Any]) -> bool:
        """Send alert via email."""
        try:
            cfg = self.config['email']
            
            msg = MIMEMultipart()
            msg['From'] = cfg['from_addr']
            msg['To'] = ', '.join(cfg['to_addrs'])
            msg['Subject'] = f"[{alert['severity'].upper()}] {alert['title']}"
            
            body = f"""
            Severity: {severity}
            Time: {time}
            
            {message}
            
            -- 
            This is an automated alert from AI-AH Monitoring.
            """.format(
                severity=alert['severity'].upper(),
                time=alert.get('timestamp', 'N/A'),
                message=alert['message']
            )
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(cfg['smtp_server'], cfg['smtp_port']) as server:
                server.starttls()
                server.login(cfg['username'], cfg['password'])
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Failed to send email alert: {e}")
            return False
    
    def _send_slack_alert(self, alert: Dict[str, Any]) -> bool:
        """Send alert to Slack."""
        try:
            cfg = self.config['slack']
            
            # Format message with emoji based on severity
            emoji = {
                'critical': ':red_circle:',
                'high': ':large_orange_diamond:',
                'medium': ':large_yellow_circle:',
                'low': ':large_blue_circle:'
            }.get(alert['severity'].lower(), ':information_source:')
            
            message = {
                'channel': cfg['channel'],
                'username': 'AI-AH Alerts',
                'icon_emoji': ':robot_face:',
                'attachments': [{
                    'color': {
                        'critical': '#ff0000',
                        'high': '#ff6600',
                        'medium': '#ffcc00',
                        'low': '#0066ff'
                    }.get(alert['severity'].lower(), '#666666'),
                    'title': f"{emoji} {alert['title']}",
                    'text': alert['message'],
                    'footer': 'AI-AH Monitoring',
                    'ts': alert.get('timestamp', '')
                }]
            }
            
            response = requests.post(
                cfg['webhook_url'],
                json=message,
                headers={'Content-Type': 'application/json'}
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Failed to send Slack alert: {e}")
            return False

def main():
    """Run alert checks and send notifications."""
    print("🔔 Checking for alerts...")
    
    manager = AlertManager()
    alerts = manager.check_metrics()
    
    if not alerts:
        print("✅ No alerts to send")
        return
    
    print(f"⚠️  Found {len(alerts)} alerts")
    
    for alert in alerts:
        print(f"\n📢 {alert['severity'].upper()}: {alert['title']}")
        print(f"   {alert['message']}")
        
        if manager.send_alert(alert):
            print("   ✅ Alert sent successfully")
        else:
            print("   ❌ Failed to send alert")

if __name__ == "__main__":
    main()
