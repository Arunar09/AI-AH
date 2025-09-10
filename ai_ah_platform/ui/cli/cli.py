#!/usr/bin/env python3
"""
CLI interface for the AI-AH Multi-Agent Infrastructure Intelligence Platform.

This module provides a command-line interface for interacting with the platform
and its specialized agents.
"""

import argparse
import asyncio
import json
import sys
import os
from typing import Dict, Any, Optional
import requests
import websocket
from datetime import datetime
import yaml


class AIAHCLI:
    """Command-line interface for the AI-AH platform."""
    
    def __init__(self, api_base_url: str = "http://localhost:8000/api/v1"):
        self.api_base_url = api_base_url
        self.ws_url = "ws://localhost:8000/ws/connect"
        self.auth_token = None
        self.session_id = f"cli_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def api_call(self, endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make an API call to the platform."""
        url = f"{self.api_base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    def login(self, username: str, password: str) -> bool:
        """Login to the platform."""
        try:
            response = self.api_call("/auth/login", "POST", {
                "username": username,
                "password": password
            })
            
            self.auth_token = response["access_token"]
            print(f"✅ Logged in as {response['user']['username']}")
            return True
        
        except Exception as e:
            print(f"❌ Login failed: {e}", file=sys.stderr)
            return False
    
    def logout(self):
        """Logout from the platform."""
        if self.auth_token:
            try:
                self.api_call("/auth/logout", "POST")
                print("✅ Logged out successfully")
            except Exception as e:
                print(f"⚠️ Logout warning: {e}")
            finally:
                self.auth_token = None
    
    def get_platform_status(self) -> Dict[str, Any]:
        """Get platform status."""
        return self.api_call("/platform/status")
    
    def get_agent_status(self, agent_type: str) -> Dict[str, Any]:
        """Get status of a specific agent."""
        return self.api_call(f"/agents/{agent_type}/status")
    
    def list_agents(self) -> Dict[str, Any]:
        """List all available agents."""
        return self.api_call("/agents/")
    
    def analyze_requirements(self, agent_type: str, requirements: str) -> Dict[str, Any]:
        """Analyze requirements with a specific agent."""
        return self.api_call(f"/agents/{agent_type}/analyze", "POST", requirements)
    
    def generate_plan(self, agent_type: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a plan with a specific agent."""
        return self.api_call(f"/agents/{agent_type}/generate", "POST", analysis)
    
    def execute_plan(self, agent_type: str, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a plan with a specific agent."""
        return self.api_call(f"/agents/{agent_type}/execute", "POST", plan)
    
    def chat_with_agent(self, message: str, agent_type: str = None) -> Dict[str, Any]:
        """Chat with an agent."""
        data = {
            "message": message,
            "user_id": "cli_user",
            "session_id": self.session_id
        }
        
        if agent_type:
            data["agent_type"] = agent_type
        
        return self.api_call("/agents/conversation", "POST", data)
    
    def terraform_request(self, requirements: str, cloud_provider: str = None, region: str = None) -> Dict[str, Any]:
        """Make a Terraform infrastructure request."""
        data = {
            "request_id": f"cli_req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_id": "cli_user",
            "requirements": requirements,
            "context": {}
        }
        
        if cloud_provider:
            data["context"]["cloud_provider"] = cloud_provider
        if region:
            data["context"]["region"] = region
        
        return self.api_call("/agents/terraform/request", "POST", data)
    
    def ansible_request(self, requirements: str, target_hosts: list = None) -> Dict[str, Any]:
        """Make an Ansible configuration request."""
        data = {
            "request_id": f"cli_req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_id": "cli_user",
            "requirements": requirements,
            "context": {}
        }
        
        if target_hosts:
            data["target_hosts"] = target_hosts
        
        return self.api_call("/agents/ansible/request", "POST", data)
    
    def kubernetes_request(self, requirements: str, namespace: str = None) -> Dict[str, Any]:
        """Make a Kubernetes orchestration request."""
        data = {
            "request_id": f"cli_req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_id": "cli_user",
            "requirements": requirements,
            "context": {}
        }
        
        if namespace:
            data["namespace"] = namespace
        
        return self.api_call("/agents/kubernetes/request", "POST", data)
    
    def security_request(self, requirements: str, compliance_framework: str = None) -> Dict[str, Any]:
        """Make a security and compliance request."""
        data = {
            "request_id": f"cli_req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_id": "cli_user",
            "requirements": requirements,
            "context": {}
        }
        
        if compliance_framework:
            data["compliance_framework"] = compliance_framework
        
        return self.api_call("/agents/security/request", "POST", data)
    
    def monitoring_request(self, requirements: str, monitoring_type: str = None) -> Dict[str, Any]:
        """Make a monitoring and observability request."""
        data = {
            "request_id": f"cli_req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_id": "cli_user",
            "requirements": requirements,
            "context": {}
        }
        
        if monitoring_type:
            data["monitoring_type"] = monitoring_type
        
        return self.api_call("/agents/monitoring/request", "POST", data)
    
    def interactive_chat(self):
        """Start interactive chat mode."""
        print("🤖 AI-AH Platform Interactive Chat")
        print("Type 'exit' to quit, 'help' for commands")
        print("-" * 50)
        
        while True:
            try:
                message = input("\n💬 You: ").strip()
                
                if message.lower() in ['exit', 'quit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if message.lower() == 'help':
                    self.show_chat_help()
                    continue
                
                if not message:
                    continue
                
                # Send message to platform
                response = self.chat_with_agent(message)
                
                print(f"\n🤖 AI: {response['response']}")
                
                if response.get('suggestions'):
                    print("\n💡 Suggestions:")
                    for suggestion in response['suggestions']:
                        print(f"   • {suggestion}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}", file=sys.stderr)
    
    def show_chat_help(self):
        """Show help for interactive chat."""
        print("\n📖 Chat Commands:")
        print("   help          - Show this help")
        print("   exit/quit     - Exit chat mode")
        print("\n💡 Example Messages:")
        print("   'Create a web server with nginx'")
        print("   'Run a security assessment'")
        print("   'Deploy a Kubernetes application'")
        print("   'Set up monitoring for my infrastructure'")
    
    def format_output(self, data: Dict[str, Any], format_type: str = "json") -> str:
        """Format output data."""
        if format_type == "json":
            return json.dumps(data, indent=2, default=str)
        elif format_type == "yaml":
            return yaml.dump(data, default_flow_style=False)
        elif format_type == "table":
            return self.format_table(data)
        else:
            return str(data)
    
    def format_table(self, data: Dict[str, Any]) -> str:
        """Format data as a table."""
        if isinstance(data, dict):
            if "agents" in data:
                # Format agents list
                lines = ["Agent Type | Status | Capabilities"]
                lines.append("-" * 40)
                for agent in data["agents"]:
                    lines.append(f"{agent['type']:<12} | {agent['status']:<6} | {agent['capabilities']}")
                return "\n".join(lines)
            else:
                # Format key-value pairs
                lines = []
                for key, value in data.items():
                    lines.append(f"{key:<20}: {value}")
                return "\n".join(lines)
        return str(data)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI-AH Multi-Agent Infrastructure Intelligence Platform CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Login and check status
  ai-ah-cli login --username admin --password admin123
  ai-ah-cli status

  # Terraform operations
  ai-ah-cli terraform "Create a web server with nginx" --provider aws --region us-east-1

  # Ansible operations
  ai-ah-cli ansible "Configure security hardening" --hosts server1,server2

  # Kubernetes operations
  ai-ah-cli kubernetes "Deploy a web application" --namespace production

  # Security operations
  ai-ah-cli security "Run compliance check" --framework CIS

  # Monitoring operations
  ai-ah-cli monitoring "Set up infrastructure monitoring"

  # Interactive chat
  ai-ah-cli chat

  # List agents
  ai-ah-cli agents list
        """
    )
    
    parser.add_argument("--api-url", default="http://localhost:8000/api/v1",
                       help="API base URL (default: http://localhost:8000/api/v1)")
    parser.add_argument("--format", choices=["json", "yaml", "table"], default="table",
                       help="Output format (default: table)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Login command
    login_parser = subparsers.add_parser("login", help="Login to the platform")
    login_parser.add_argument("--username", required=True, help="Username")
    login_parser.add_argument("--password", required=True, help="Password")
    
    # Status command
    subparsers.add_parser("status", help="Get platform status")
    
    # Agents commands
    agents_parser = subparsers.add_parser("agents", help="Agent operations")
    agents_subparsers = agents_parser.add_subparsers(dest="agents_action")
    agents_subparsers.add_parser("list", help="List all agents")
    agents_subparsers.add_parser("status", help="Get agent status").add_argument("agent_type", help="Agent type")
    
    # Terraform command
    terraform_parser = subparsers.add_parser("terraform", help="Terraform operations")
    terraform_parser.add_argument("requirements", help="Infrastructure requirements")
    terraform_parser.add_argument("--provider", help="Cloud provider")
    terraform_parser.add_argument("--region", help="Region")
    
    # Ansible command
    ansible_parser = subparsers.add_parser("ansible", help="Ansible operations")
    ansible_parser.add_argument("requirements", help="Configuration requirements")
    ansible_parser.add_argument("--hosts", help="Target hosts (comma-separated)")
    
    # Kubernetes command
    k8s_parser = subparsers.add_parser("kubernetes", help="Kubernetes operations")
    k8s_parser.add_argument("requirements", help="Deployment requirements")
    k8s_parser.add_argument("--namespace", help="Kubernetes namespace")
    
    # Security command
    security_parser = subparsers.add_parser("security", help="Security operations")
    security_parser.add_argument("requirements", help="Security requirements")
    security_parser.add_argument("--framework", help="Compliance framework")
    
    # Monitoring command
    monitoring_parser = subparsers.add_parser("monitoring", help="Monitoring operations")
    monitoring_parser.add_argument("requirements", help="Monitoring requirements")
    monitoring_parser.add_argument("--type", help="Monitoring type")
    
    # Chat command
    subparsers.add_parser("chat", help="Interactive chat mode")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize CLI
    cli = AIAHCLI(args.api_url)
    
    try:
        if args.command == "login":
            success = cli.login(args.username, args.password)
            if not success:
                sys.exit(1)
        
        elif args.command == "status":
            status = cli.get_platform_status()
            print(cli.format_output(status, args.format))
        
        elif args.command == "agents":
            if args.agents_action == "list":
                agents = cli.list_agents()
                print(cli.format_output(agents, args.format))
            elif args.agents_action == "status":
                status = cli.get_agent_status(args.agent_type)
                print(cli.format_output(status, args.format))
        
        elif args.command == "terraform":
            response = cli.terraform_request(args.requirements, args.provider, args.region)
            print(cli.format_output(response, args.format))
        
        elif args.command == "ansible":
            hosts = args.hosts.split(",") if args.hosts else None
            response = cli.ansible_request(args.requirements, hosts)
            print(cli.format_output(response, args.format))
        
        elif args.command == "kubernetes":
            response = cli.kubernetes_request(args.requirements, args.namespace)
            print(cli.format_output(response, args.format))
        
        elif args.command == "security":
            response = cli.security_request(args.requirements, args.framework)
            print(cli.format_output(response, args.format))
        
        elif args.command == "monitoring":
            response = cli.monitoring_request(args.requirements, args.type)
            print(cli.format_output(response, args.format))
        
        elif args.command == "chat":
            cli.interactive_chat()
        
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        if cli.auth_token:
            cli.logout()


if __name__ == "__main__":
    main()
