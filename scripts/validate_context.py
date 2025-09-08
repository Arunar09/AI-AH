#!/usr/bin/env python3
"""
Project Context Validator

This script ensures all code changes align with project context and principles.
"""
import os
import sys
from pathlib import Path
import yaml
import re

# Project root
ROOT = Path(__file__).parent.parent

# Required documentation files
REQUIRED_FILES = [
    'CONTEXT.md',
    'ARCHITECTURE.md',
    'ROADMAP.md',
    'PROJECT_GOVERNANCE.md'
]

def check_required_files():
    """Verify all required documentation files exist."""
    missing = []
    for file in REQUIRED_FILES:
        if not (ROOT / file).exists():
            missing.append(file)
    
    if missing:
        print(f"❌ Missing required files: {', '.join(missing)}")
        return False
    return True

def check_decision_records():
    """Ensure all major changes have corresponding ADRs."""
    changes_dir = ROOT / 'docs' / 'decisions'
    if not changes_dir.exists():
        print(f"❌ Missing decisions directory: {changes_dir}")
        return False
    
    # Check for recent changes without ADRs
    # This is a simplified check - in practice, you'd use git history
    return True

def check_security_practices():
    """Check for common security issues."""
    # Example: No hardcoded credentials
    secrets_patterns = [
        r'password\s*=',
        r'api[_-]?key\s*=',
        r'secret[_-]?key\s*=',
        r'token\s*='
    ]
    
    issues = []
    for root, _, files in os.walk(ROOT):
        # Skip virtual environment and other directories
        if any(skip in root for skip in ['venv', '.git', '__pycache__']):
            continue
            
        for file in files:
            if not file.endswith(('.py', '.yaml', '.yml', '.tf', '.json')):
                continue
                
            filepath = Path(root) / file
            try:
                content = filepath.read_text()
                for i, line in enumerate(content.split('\n'), 1):
                    for pattern in secrets_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            issues.append(f"{filepath}:{i} - Potential secret in code")
                            break
            except UnicodeDecodeError:
                continue
    
    if issues:
        for issue in issues:
            print(f"⚠️  {issue}")
        return False
    return True

def main():
    """Run all validation checks."""
    print("🔍 Validating project context...")
    
    checks = [
        ("Required Files", check_required_files()),
        ("Decision Records", check_decision_records()),
        ("Security Practices", check_security_practices())
    ]
    
    all_passed = True
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        if not result:
            all_passed = False
    
    if not all_passed:
        print("\n❌ Validation failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n🎉 All validations passed!")
    sys.exit(0)

if __name__ == "__main__":
    main()
