#!/usr/bin/env python3
"""
Infrastructure Metrics Collector

Collects metrics specific to infrastructure management:
- Terraform state analysis
- Resource inventory
- Security findings
- Cost estimates
"""
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

class InfraMetricsCollector:
    def __init__(self, workspace_dir: str = 'web_terraform_workspace'):
        self.workspace_dir = Path(workspace_dir)
        self.metrics: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat(),
            'infrastructure': {}
        }
        
    def collect_all(self) -> Dict[str, Any]:
        """Collect all infrastructure metrics."""
        self._collect_terraform_metrics()
        self._collect_security_metrics()
        self._collect_cost_metrics()
        return self.metrics
    
    def _collect_terraform_metrics(self) -> None:
        """Collect metrics from Terraform state and plan."""
        try:
            # Get Terraform state
            state = self._run_terraform('state list')
            resources = state.split('\n') if state else []
            
            # Categorize resources
            resource_types = {}
            for res in resources:
                if not res.strip():
                    continue
                res_type = res.split('.')[0]
                resource_types[res_type] = resource_types.get(res_type, 0) + 1
            
            # Get Terraform version
            version_output = self._run_terraform('version')
            version = version_output.split('\n')[0] if version_output else 'unknown'
            
            self.metrics['infrastructure'].update({
                'terraform': {
                    'version': version,
                    'resource_count': len(resources),
                    'resource_types': resource_types,
                    'workspaces': self._get_workspaces()
                }
            })
            
        except Exception as e:
            self.metrics['infrastructure']['terraform'] = {
                'error': str(e)
            }
    
    def _collect_security_metrics(self) -> None:
        """Collect security-related metrics."""
        try:
            # This would be integrated with tools like Checkov, TFLint, etc.
            self.metrics['infrastructure']['security'] = {
                'scans': {
                    'last_scan': datetime.utcnow().isoformat(),
                    'critical_findings': 0,  # Placeholder
                    'high_findings': 0,      # Placeholder
                    'medium_findings': 0,     # Placeholder
                    'low_findings': 0         # Placeholder
                },
                'compliance': {
                    'cis_benchmark': 'pending',
                    'gdpr': 'pending',
                    'hipaa': 'pending'
                }
            }
        except Exception as e:
            self.metrics['infrastructure']['security'] = {
                'error': str(e)
            }
    
    def _collect_cost_metrics(self) -> None:
        """Collect cost estimation metrics."""
        try:
            # This would integrate with Terraform Cloud, Infracost, or cloud provider APIs
            self.metrics['infrastructure']['cost'] = {
                'monthly_estimate': {
                    'total': 0.0,  # Placeholder
                    'by_service': {}
                },
                'budget': {
                    'monthly_budget': 0.0,  # Should be configured
                    'forecast_overspend': False
                }
            }
        except Exception as e:
            self.metrics['infrastructure']['cost'] = {
                'error': str(e)
            }
    
    def _get_workspaces(self) -> List[str]:
        """List all Terraform workspaces."""
        try:
            output = self._run_terraform('workspace list')
            return [line.strip('* ') for line in output.split('\n') if line.strip()]
        except Exception:
            return []
    
    def _run_terraform(self, command: str) -> str:
        """Run a Terraform command and return the output."""
        try:
            cmd = ['terraform', *command.split()]
            result = subprocess.run(
                cmd,
                cwd=self.workspace_dir,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running Terraform: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
            return ""
        except Exception as e:
            print(f"Unexpected error: {e}")
            return ""

def save_metrics(metrics: Dict[str, Any], output_file: str = 'metrics/infra_metrics.json') -> None:
    """Save metrics to a JSON file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"✅ Metrics saved to {output_path}")

def main():
    """Collect and save infrastructure metrics."""
    collector = InfraMetricsCollector()
    metrics = collector.collect_all()
    
    # Save metrics
    save_metrics(metrics)
    
    # Print summary
    print("\n📊 Infrastructure Metrics Summary")
    print(f"- Timestamp: {metrics['timestamp']}")
    
    if 'terraform' in metrics['infrastructure']:
        tf = metrics['infrastructure']['terraform']
        print(f"- Terraform Version: {tf.get('version', 'unknown')}")
        print(f"- Total Resources: {tf.get('resource_count', 0)}")
        print(f"- Workspaces: {', '.join(tf.get('workspaces', []))}")
    
    if 'security' in metrics['infrastructure']:
        sec = metrics['infrastructure']['security'].get('scans', {})
        print(f"- Security Findings: {sec.get('critical_findings', 0)} critical")
    
    if 'cost' in metrics['infrastructure']:
        cost = metrics['infrastructure']['cost'].get('monthly_estimate', {})
        print(f"- Monthly Cost Estimate: ${cost.get('total', 0):.2f}")

if __name__ == "__main__":
    main()
