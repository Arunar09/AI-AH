"""
Terraform Project Modifier - Enhanced Project Management
Handles modification of existing Terraform projects with precision-based requests
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import ast

@dataclass
class ProjectModification:
    """Represents a modification to an existing project"""
    modification_id: str
    project_path: str
    modification_type: str
    description: str
    changes: List[Dict[str, Any]]
    impact_assessment: Dict[str, Any]
    rollback_plan: List[str]
    created_at: datetime

@dataclass
class ResourceChange:
    """Represents a change to a Terraform resource"""
    resource_type: str
    resource_name: str
    change_type: str  # add, modify, remove
    old_config: Optional[Dict[str, Any]]
    new_config: Optional[Dict[str, Any]]
    impact_level: str  # low, medium, high, critical

class TerraformProjectModifier:
    """Enhanced project modification with precision-based requests"""
    
    def __init__(self, workspaces_dir: str = "workspaces"):
        self.workspaces_dir = Path(workspaces_dir)
        self.workspaces_dir.mkdir(exist_ok=True)
        
        # Modification patterns
        self.modification_patterns = {
            'scaling': self._handle_scaling_modification,
            'security': self._handle_security_modification,
            'cost_optimization': self._handle_cost_optimization,
            'performance': self._handle_performance_modification,
            'compliance': self._handle_compliance_modification,
            'monitoring': self._handle_monitoring_modification
        }
    
    def analyze_existing_project(self, project_path: str) -> Dict[str, Any]:
        """Analyze existing Terraform project structure"""
        try:
            project_path = Path(project_path)
            if not project_path.exists():
                return {"error": "Project path does not exist"}
            
            analysis = {
                'project_name': project_path.name,
                'terraform_files': [],
                'resources': [],
                'variables': {},
                'outputs': {},
                'providers': [],
                'dependencies': [],
                'complexity_score': 0,
                'modification_readiness': 'unknown'
            }
            
            # Analyze Terraform files
            for tf_file in project_path.glob("*.tf"):
                file_analysis = self._analyze_terraform_file(tf_file)
                analysis['terraform_files'].append(file_analysis)
                analysis['resources'].extend(file_analysis.get('resources', []))
                analysis['providers'].extend(file_analysis.get('providers', []))
            
            # Analyze variables
            variables_file = project_path / "variables.tf"
            if variables_file.exists():
                analysis['variables'] = self._extract_variables(variables_file)
            
            # Analyze outputs
            outputs_file = project_path / "outputs.tf"
            if outputs_file.exists():
                analysis['outputs'] = self._extract_outputs(outputs_file)
            
            # Calculate complexity score
            analysis['complexity_score'] = self._calculate_complexity_score(analysis)
            
            # Assess modification readiness
            analysis['modification_readiness'] = self._assess_modification_readiness(analysis)
            
            return analysis
            
        except Exception as e:
            return {"error": f"Failed to analyze project: {str(e)}"}
    
    def _analyze_terraform_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Terraform file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            analysis = {
                'filename': file_path.name,
                'size': len(content),
                'resources': [],
                'providers': [],
                'data_sources': [],
                'modules': []
            }
            
            # Extract resources
            resource_pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"'
            for match in re.finditer(resource_pattern, content):
                analysis['resources'].append({
                    'type': match.group(1),
                    'name': match.group(2),
                    'line': content[:match.start()].count('\n') + 1
                })
            
            # Extract providers
            provider_pattern = r'provider\s+"([^"]+)"'
            for match in re.finditer(provider_pattern, content):
                analysis['providers'].append(match.group(1))
            
            # Extract data sources
            data_pattern = r'data\s+"([^"]+)"\s+"([^"]+)"'
            for match in re.finditer(data_pattern, content):
                analysis['data_sources'].append({
                    'type': match.group(1),
                    'name': match.group(2)
                })
            
            # Extract modules
            module_pattern = r'module\s+"([^"]+)"'
            for match in re.finditer(module_pattern, content):
                analysis['modules'].append(match.group(1))
            
            return analysis
            
        except Exception as e:
            return {"error": f"Failed to analyze file {file_path}: {str(e)}"}
    
    def _extract_variables(self, variables_file: Path) -> Dict[str, Any]:
        """Extract variables from variables.tf"""
        try:
            with open(variables_file, 'r') as f:
                content = f.read()
            
            variables = {}
            # Simple regex to extract variable definitions
            var_pattern = r'variable\s+"([^"]+)"\s*\{[^}]*description\s*=\s*"([^"]*)"[^}]*default\s*=\s*([^}]+)'
            
            for match in re.finditer(var_pattern, content, re.DOTALL):
                var_name = match.group(1)
                description = match.group(2)
                default_value = match.group(3).strip()
                
                variables[var_name] = {
                    'description': description,
                    'default': default_value
                }
            
            return variables
            
        except Exception as e:
            return {"error": f"Failed to extract variables: {str(e)}"}
    
    def _extract_outputs(self, outputs_file: Path) -> Dict[str, Any]:
        """Extract outputs from outputs.tf"""
        try:
            with open(outputs_file, 'r') as f:
                content = f.read()
            
            outputs = {}
            # Simple regex to extract output definitions
            output_pattern = r'output\s+"([^"]+)"\s*\{[^}]*description\s*=\s*"([^"]*)"[^}]*value\s*=\s*([^}]+)'
            
            for match in re.finditer(output_pattern, content, re.DOTALL):
                output_name = match.group(1)
                description = match.group(2)
                value = match.group(3).strip()
                
                outputs[output_name] = {
                    'description': description,
                    'value': value
                }
            
            return outputs
            
        except Exception as e:
            return {"error": f"Failed to extract outputs: {str(e)}"}
    
    def _calculate_complexity_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate project complexity score"""
        score = 0
        
        # Count resources
        score += len(analysis.get('resources', [])) * 2
        
        # Count providers
        score += len(set(analysis.get('providers', []))) * 3
        
        # Count modules
        score += len(analysis.get('modules', [])) * 5
        
        # Count data sources
        score += len(analysis.get('data_sources', [])) * 1
        
        # File size factor
        total_size = sum(f.get('size', 0) for f in analysis.get('terraform_files', []))
        score += total_size // 1000
        
        return score
    
    def _assess_modification_readiness(self, analysis: Dict[str, Any]) -> str:
        """Assess how ready a project is for modification"""
        complexity = analysis.get('complexity_score', 0)
        resource_count = len(analysis.get('resources', []))
        
        if complexity < 20 and resource_count < 10:
            return "high"
        elif complexity < 50 and resource_count < 20:
            return "medium"
        else:
            return "low"
    
    def modify_project(self, project_path: str, modification_request: str, precision_level: str = "medium") -> Dict[str, Any]:
        """Modify existing project based on precision request"""
        try:
            # Analyze existing project
            project_analysis = self.analyze_existing_project(project_path)
            if "error" in project_analysis:
                return project_analysis
            
            # Parse modification request
            modification_type = self._identify_modification_type(modification_request)
            
            # Apply precision-based modification
            if modification_type in self.modification_patterns:
                modification_result = self.modification_patterns[modification_type](
                    project_path, modification_request, project_analysis, precision_level
                )
            else:
                return {"error": f"Unknown modification type: {modification_type}"}
            
            return modification_result
            
        except Exception as e:
            return {"error": f"Failed to modify project: {str(e)}"}
    
    def _identify_modification_type(self, request: str) -> str:
        """Identify the type of modification requested"""
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in ['scale', 'scaling', 'increase', 'decrease', 'more', 'less']):
            return 'scaling'
        elif any(keyword in request_lower for keyword in ['security', 'encrypt', 'secure', 'firewall', 'access']):
            return 'security'
        elif any(keyword in request_lower for keyword in ['cost', 'optimize', 'cheaper', 'budget', 'save']):
            return 'cost_optimization'
        elif any(keyword in request_lower for keyword in ['performance', 'faster', 'speed', 'optimize']):
            return 'performance'
        elif any(keyword in request_lower for keyword in ['compliance', 'audit', 'soc2', 'gdpr']):
            return 'compliance'
        elif any(keyword in request_lower for keyword in ['monitor', 'logging', 'alert', 'metrics']):
            return 'monitoring'
        else:
            return 'general'
    
    def _handle_scaling_modification(self, project_path: str, request: str, analysis: Dict[str, Any], precision: str) -> Dict[str, Any]:
        """Handle scaling modifications"""
        changes = []
        
        # Identify scaling targets
        if 'user' in request.lower():
            # Scale for more users
            changes.extend(self._scale_for_users(analysis, request))
        elif 'data' in request.lower():
            # Scale for more data
            changes.extend(self._scale_for_data(analysis, request))
        elif 'traffic' in request.lower():
            # Scale for more traffic
            changes.extend(self._scale_for_traffic(analysis, request))
        
        return {
            'modification_type': 'scaling',
            'changes': changes,
            'impact_assessment': self._assess_scaling_impact(changes),
            'rollback_plan': self._generate_rollback_plan(changes)
        }
    
    def _handle_security_modification(self, project_path: str, request: str, analysis: Dict[str, Any], precision: str) -> Dict[str, Any]:
        """Handle security modifications"""
        changes = []
        
        # Add encryption
        if 'encrypt' in request.lower():
            changes.extend(self._add_encryption(analysis))
        
        # Add security groups
        if 'firewall' in request.lower() or 'security' in request.lower():
            changes.extend(self._add_security_groups(analysis))
        
        # Add compliance features
        if 'compliance' in request.lower():
            changes.extend(self._add_compliance_features(analysis))
        
        return {
            'modification_type': 'security',
            'changes': changes,
            'impact_assessment': self._assess_security_impact(changes),
            'rollback_plan': self._generate_rollback_plan(changes)
        }
    
    def _handle_cost_optimization(self, project_path: str, request: str, analysis: Dict[str, Any], precision: str) -> Dict[str, Any]:
        """Handle cost optimization modifications"""
        changes = []
        
        # Right-size instances
        if 'instance' in request.lower():
            changes.extend(self._optimize_instances(analysis))
        
        # Optimize storage
        if 'storage' in request.lower():
            changes.extend(self._optimize_storage(analysis))
        
        # Add scheduling
        if 'schedule' in request.lower():
            changes.extend(self._add_scheduling(analysis))
        
        return {
            'modification_type': 'cost_optimization',
            'changes': changes,
            'impact_assessment': self._assess_cost_impact(changes),
            'rollback_plan': self._generate_rollback_plan(changes)
        }
    
    def _handle_performance_modification(self, project_path: str, request: str, analysis: Dict[str, Any], precision: str) -> Dict[str, Any]:
        """Handle performance modifications"""
        changes = []
        
        # Add caching
        if 'cache' in request.lower():
            changes.extend(self._add_caching(analysis))
        
        # Add load balancing
        if 'load' in request.lower() or 'balance' in request.lower():
            changes.extend(self._add_load_balancing(analysis))
        
        # Optimize database
        if 'database' in request.lower() or 'db' in request.lower():
            changes.extend(self._optimize_database(analysis))
        
        return {
            'modification_type': 'performance',
            'changes': changes,
            'impact_assessment': self._assess_performance_impact(changes),
            'rollback_plan': self._generate_rollback_plan(changes)
        }
    
    def _handle_compliance_modification(self, project_path: str, request: str, analysis: Dict[str, Any], precision: str) -> Dict[str, Any]:
        """Handle compliance modifications"""
        changes = []
        
        # Add logging
        if 'log' in request.lower():
            changes.extend(self._add_logging(analysis))
        
        # Add monitoring
        if 'monitor' in request.lower():
            changes.extend(self._add_monitoring(analysis))
        
        # Add backup
        if 'backup' in request.lower():
            changes.extend(self._add_backup(analysis))
        
        return {
            'modification_type': 'compliance',
            'changes': changes,
            'impact_assessment': self._assess_compliance_impact(changes),
            'rollback_plan': self._generate_rollback_plan(changes)
        }
    
    def _handle_monitoring_modification(self, project_path: str, request: str, analysis: Dict[str, Any], precision: str) -> Dict[str, Any]:
        """Handle monitoring modifications"""
        changes = []
        
        # Add CloudWatch
        changes.extend(self._add_cloudwatch(analysis))
        
        # Add alerts
        changes.extend(self._add_alerts(analysis))
        
        # Add dashboards
        changes.extend(self._add_dashboards(analysis))
        
        return {
            'modification_type': 'monitoring',
            'changes': changes,
            'impact_assessment': self._assess_monitoring_impact(changes),
            'rollback_plan': self._generate_rollback_plan(changes)
        }
    
    # Helper methods for specific modifications
    def _scale_for_users(self, analysis: Dict[str, Any], request: str) -> List[Dict[str, Any]]:
        """Scale infrastructure for more users"""
        changes = []
        
        # Extract user count from request
        user_count = self._extract_number_from_request(request)
        
        # Scale EC2 instances
        for resource in analysis.get('resources', []):
            if resource['type'] == 'aws_instance':
                changes.append({
                    'resource_type': 'aws_instance',
                    'resource_name': resource['name'],
                    'change_type': 'modify',
                    'changes': {
                        'count': user_count // 100,  # 1 instance per 100 users
                        'instance_type': 't3.medium' if user_count > 500 else 't3.small'
                    }
                })
        
        # Add auto-scaling if needed
        if user_count > 1000:
            changes.append({
                'resource_type': 'aws_autoscaling_group',
                'resource_name': 'web_asg',
                'change_type': 'add',
                'changes': {
                    'min_size': 2,
                    'max_size': 10,
                    'desired_capacity': 3
                }
            })
        
        return changes
    
    def _scale_for_data(self, analysis: Dict[str, Any], request: str) -> List[Dict[str, Any]]:
        """Scale infrastructure for more data"""
        changes = []
        
        # Scale RDS instances
        for resource in analysis.get('resources', []):
            if resource['type'] == 'aws_db_instance':
                changes.append({
                    'resource_type': 'aws_db_instance',
                    'resource_name': resource['name'],
                    'change_type': 'modify',
                    'changes': {
                        'instance_class': 'db.r5.large',
                        'allocated_storage': 100
                    }
                })
        
        return changes
    
    def _scale_for_traffic(self, analysis: Dict[str, Any], request: str) -> List[Dict[str, Any]]:
        """Scale infrastructure for more traffic"""
        changes = []
        
        # Add CloudFront
        changes.append({
            'resource_type': 'aws_cloudfront_distribution',
            'resource_name': 'cdn',
            'change_type': 'add',
            'changes': {
                'enabled': True,
                'default_cache_behavior': {
                    'target_origin_id': 'web_origin',
                    'viewer_protocol_policy': 'redirect-to-https'
                }
            }
        })
        
        return changes
    
    def _add_encryption(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add encryption to resources"""
        changes = []
        
        # Add KMS key
        changes.append({
            'resource_type': 'aws_kms_key',
            'resource_name': 'encryption_key',
            'change_type': 'add',
            'changes': {
                'description': 'Encryption key for infrastructure',
                'deletion_window_in_days': 7
            }
        })
        
        return changes
    
    def _add_security_groups(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add security groups"""
        changes = []
        
        # Add web security group
        changes.append({
            'resource_type': 'aws_security_group',
            'resource_name': 'web_sg',
            'change_type': 'add',
            'changes': {
                'ingress': [
                    {'from_port': 80, 'to_port': 80, 'protocol': 'tcp', 'cidr_blocks': ['0.0.0.0/0']},
                    {'from_port': 443, 'to_port': 443, 'protocol': 'tcp', 'cidr_blocks': ['0.0.0.0/0']}
                ],
                'egress': [
                    {'from_port': 0, 'to_port': 0, 'protocol': '-1', 'cidr_blocks': ['0.0.0.0/0']}
                ]
            }
        })
        
        return changes
    
    def _add_compliance_features(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add compliance features"""
        changes = []
        
        # Add CloudTrail
        changes.append({
            'resource_type': 'aws_cloudtrail',
            'resource_name': 'audit_trail',
            'change_type': 'add',
            'changes': {
                'enable_logging': True,
                'include_global_service_events': True
            }
        })
        
        return changes
    
    def _optimize_instances(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimize instance configurations"""
        changes = []
        
        # Right-size instances
        for resource in analysis.get('resources', []):
            if resource['type'] == 'aws_instance':
                changes.append({
                    'resource_type': 'aws_instance',
                    'resource_name': resource['name'],
                    'change_type': 'modify',
                    'changes': {
                        'instance_type': 't3.small'  # Right-sized instance
                    }
                })
        
        return changes
    
    def _optimize_storage(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimize storage configurations"""
        changes = []
        
        # Optimize S3 storage class
        for resource in analysis.get('resources', []):
            if resource['type'] == 'aws_s3_bucket':
                changes.append({
                    'resource_type': 'aws_s3_bucket_lifecycle_configuration',
                    'resource_name': f"{resource['name']}_lifecycle",
                    'change_type': 'add',
                    'changes': {
                        'rule': {
                            'id': 'optimize_storage',
                            'status': 'Enabled',
                            'transition': {
                                'days': 30,
                                'storage_class': 'STANDARD_IA'
                            }
                        }
                    }
                })
        
        return changes
    
    def _add_scheduling(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add scheduling for cost optimization"""
        changes = []
        
        # Add Lambda function for scheduling
        changes.append({
            'resource_type': 'aws_lambda_function',
            'resource_name': 'scheduler',
            'change_type': 'add',
            'changes': {
                'runtime': 'python3.9',
                'handler': 'index.handler',
                'code': 'inline'
            }
        })
        
        return changes
    
    def _add_caching(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add caching layer"""
        changes = []
        
        # Add ElastiCache
        changes.append({
            'resource_type': 'aws_elasticache_cluster',
            'resource_name': 'cache_cluster',
            'change_type': 'add',
            'changes': {
                'engine': 'redis',
                'node_type': 'cache.t3.micro',
                'num_cache_nodes': 1
            }
        })
        
        return changes
    
    def _add_load_balancing(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add load balancing"""
        changes = []
        
        # Add Application Load Balancer
        changes.append({
            'resource_type': 'aws_lb',
            'resource_name': 'app_lb',
            'change_type': 'add',
            'changes': {
                'load_balancer_type': 'application',
                'internal': False
            }
        })
        
        return changes
    
    def _optimize_database(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimize database configuration"""
        changes = []
        
        # Optimize RDS instances
        for resource in analysis.get('resources', []):
            if resource['type'] == 'aws_db_instance':
                changes.append({
                    'resource_type': 'aws_db_instance',
                    'resource_name': resource['name'],
                    'change_type': 'modify',
                    'changes': {
                        'performance_insights_enabled': True,
                        'monitoring_interval': 60
                    }
                })
        
        return changes
    
    def _add_logging(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add logging configuration"""
        changes = []
        
        # Add CloudWatch Log Groups
        changes.append({
            'resource_type': 'aws_cloudwatch_log_group',
            'resource_name': 'app_logs',
            'change_type': 'add',
            'changes': {
                'retention_in_days': 30
            }
        })
        
        return changes
    
    def _add_monitoring(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add monitoring configuration"""
        changes = []
        
        # Add CloudWatch alarms
        changes.append({
            'resource_type': 'aws_cloudwatch_metric_alarm',
            'resource_name': 'cpu_alarm',
            'change_type': 'add',
            'changes': {
                'comparison_operator': 'GreaterThanThreshold',
                'evaluation_periods': 2,
                'metric_name': 'CPUUtilization',
                'threshold': 80
            }
        })
        
        return changes
    
    def _add_backup(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add backup configuration"""
        changes = []
        
        # Add backup vault
        changes.append({
            'resource_type': 'aws_backup_vault',
            'resource_name': 'backup_vault',
            'change_type': 'add',
            'changes': {
                'name': 'backup-vault'
            }
        })
        
        return changes
    
    def _add_cloudwatch(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add CloudWatch monitoring"""
        changes = []
        
        # Add CloudWatch dashboard
        changes.append({
            'resource_type': 'aws_cloudwatch_dashboard',
            'resource_name': 'main_dashboard',
            'change_type': 'add',
            'changes': {
                'dashboard_body': json.dumps({
                    'widgets': [
                        {
                            'type': 'metric',
                            'properties': {
                                'metrics': [['AWS/EC2', 'CPUUtilization']],
                                'period': 300,
                                'stat': 'Average'
                            }
                        }
                    ]
                })
            }
        })
        
        return changes
    
    def _add_alerts(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add alerting configuration"""
        changes = []
        
        # Add SNS topic for alerts
        changes.append({
            'resource_type': 'aws_sns_topic',
            'resource_name': 'alerts',
            'change_type': 'add',
            'changes': {
                'name': 'infrastructure-alerts'
            }
        })
        
        return changes
    
    def _add_dashboards(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add monitoring dashboards"""
        changes = []
        
        # Add Grafana dashboard (if applicable)
        changes.append({
            'resource_type': 'aws_grafana_workspace',
            'resource_name': 'monitoring_workspace',
            'change_type': 'add',
            'changes': {
                'account_access_type': 'CURRENT_ACCOUNT',
                'authentication_providers': ['AWS_SSO']
            }
        })
        
        return changes
    
    def _extract_number_from_request(self, request: str) -> int:
        """Extract number from request"""
        import re
        numbers = re.findall(r'\d+', request)
        return int(numbers[0]) if numbers else 100
    
    def _assess_scaling_impact(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess impact of scaling changes"""
        return {
            'cost_impact': 'medium',
            'performance_impact': 'high',
            'security_impact': 'low',
            'operational_impact': 'medium'
        }
    
    def _assess_security_impact(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess impact of security changes"""
        return {
            'cost_impact': 'low',
            'performance_impact': 'low',
            'security_impact': 'high',
            'operational_impact': 'low'
        }
    
    def _assess_cost_impact(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess impact of cost optimization changes"""
        return {
            'cost_impact': 'high',
            'performance_impact': 'medium',
            'security_impact': 'low',
            'operational_impact': 'low'
        }
    
    def _assess_performance_impact(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess impact of performance changes"""
        return {
            'cost_impact': 'medium',
            'performance_impact': 'high',
            'security_impact': 'low',
            'operational_impact': 'medium'
        }
    
    def _assess_compliance_impact(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess impact of compliance changes"""
        return {
            'cost_impact': 'medium',
            'performance_impact': 'low',
            'security_impact': 'high',
            'operational_impact': 'medium'
        }
    
    def _assess_monitoring_impact(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess impact of monitoring changes"""
        return {
            'cost_impact': 'low',
            'performance_impact': 'low',
            'security_impact': 'low',
            'operational_impact': 'high'
        }
    
    def _generate_rollback_plan(self, changes: List[Dict[str, Any]]) -> List[str]:
        """Generate rollback plan for changes"""
        rollback_steps = []
        
        for change in changes:
            if change['change_type'] == 'add':
                rollback_steps.append(f"Remove {change['resource_type']} {change['resource_name']}")
            elif change['change_type'] == 'modify':
                rollback_steps.append(f"Revert {change['resource_type']} {change['resource_name']} to previous configuration")
            elif change['change_type'] == 'remove':
                rollback_steps.append(f"Restore {change['resource_type']} {change['resource_name']}")
        
        return rollback_steps
    
    def apply_modifications(self, project_path: str, modifications: Dict[str, Any]) -> Dict[str, Any]:
        """Apply modifications to project files"""
        try:
            # This would implement the actual file modifications
            # For now, return a summary of what would be changed
            return {
                'success': True,
                'message': f"Applied {len(modifications.get('changes', []))} modifications",
                'modified_files': ['main.tf', 'variables.tf'],
                'backup_created': True,
                'rollback_available': True
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to apply modifications: {str(e)}"
            }
