#!/usr/bin/env python3
"""
AI-AH Lab Runner
Main script to run the local lab environment
"""

import os
import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="AI-AH Local Lab Runner")
    parser.add_argument("command", choices=["setup", "test", "deploy", "cleanup"], 
                       help="Command to run")
    parser.add_argument("--environment", choices=["basic", "advanced", "production"],
                       default="basic", help="Environment to use")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Run in dry-run mode (no actual deployment)")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        print("🏗️ Setting up lab environment...")
        from setup_local_lab import LocalLabSetup
        lab = LocalLabSetup()
        lab.setup_lab_directories()
        lab.create_terraform_modules()
        lab.create_lab_environments()
        lab.create_docker_compose()
        lab.create_test_scripts()
        lab.create_agent_test_framework()
        print("✅ Lab setup complete!")
        
    elif args.command == "test":
        print(f"🧪 Testing {args.environment} environment...")
        
        if args.dry_run:
            print("🔍 Running in dry-run mode...")
            os.system(f"cd lab/terraform/environments/{args.environment} && terraform plan")
        else:
            print("🚀 Running full test...")
            os.system(f"cd lab && python test_agents.py")
            
    elif args.command == "deploy":
        print(f"🚀 Deploying {args.environment} environment...")
        
        if args.dry_run:
            print("🔍 Planning deployment...")
            os.system(f"cd lab/terraform/environments/{args.environment} && terraform plan")
        else:
            print("⚠️ This will create real AWS resources. Continue? (y/N)")
            if input().lower() == 'y':
                os.system(f"cd lab/terraform/environments/{args.environment} && terraform apply")
            else:
                print("❌ Deployment cancelled")
                
    elif args.command == "cleanup":
        print(f"🧹 Cleaning up {args.environment} environment...")
        
        if args.dry_run:
            print("🔍 Planning cleanup...")
            os.system(f"cd lab/terraform/environments/{args.environment} && terraform plan -destroy")
        else:
            print("⚠️ This will destroy AWS resources. Continue? (y/N)")
            if input().lower() == 'y':
                os.system(f"cd lab/terraform/environments/{args.environment} && terraform destroy")
            else:
                print("❌ Cleanup cancelled")

if __name__ == "__main__":
    main()
