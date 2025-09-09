#!/usr/bin/env python3
"""
Test runner for the AI-AH Multi-Agent Infrastructure Intelligence Platform.

This script provides a convenient way to run different types of tests
with various configurations and options.
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {command[0]}")
        return False


def run_unit_tests(verbose=False, coverage=False):
    """Run unit tests."""
    command = ["python", "-m", "pytest", "tests/test_core_framework.py", "-m", "unit"]
    
    if verbose:
        command.append("-v")
    
    if coverage:
        command.extend(["--cov=platform", "--cov-report=html", "--cov-report=term-missing"])
    
    return run_command(command, "Unit Tests")


def run_agent_tests(verbose=False, coverage=False):
    """Run agent tests."""
    command = ["python", "-m", "pytest", "tests/test_agents.py", "-m", "unit"]
    
    if verbose:
        command.append("-v")
    
    if coverage:
        command.extend(["--cov=platform.agents", "--cov-report=html", "--cov-report=term-missing"])
    
    return run_command(command, "Agent Tests")


def run_api_tests(verbose=False, coverage=False):
    """Run API tests."""
    command = ["python", "-m", "pytest", "tests/test_api.py", "-m", "api"]
    
    if verbose:
        command.append("-v")
    
    if coverage:
        command.extend(["--cov=platform.api", "--cov-report=html", "--cov-report=term-missing"])
    
    return run_command(command, "API Tests")


def run_integration_tests(verbose=False, coverage=False):
    """Run integration tests."""
    command = ["python", "-m", "pytest", "tests/test_integration.py", "-m", "integration"]
    
    if verbose:
        command.append("-v")
    
    if coverage:
        command.extend(["--cov=platform", "--cov-report=html", "--cov-report=term-missing"])
    
    return run_command(command, "Integration Tests")


def run_all_tests(verbose=False, coverage=False, exclude_slow=False):
    """Run all tests."""
    command = ["python", "-m", "pytest", "tests/"]
    
    if verbose:
        command.append("-v")
    
    if exclude_slow:
        command.extend(["-m", "not slow"])
    
    if coverage:
        command.extend(["--cov=platform", "--cov-report=html", "--cov-report=term-missing"])
    
    return run_command(command, "All Tests")


def run_specific_test(test_path, verbose=False):
    """Run a specific test file or test function."""
    command = ["python", "-m", "pytest", test_path]
    
    if verbose:
        command.append("-v")
    
    return run_command(command, f"Specific Test: {test_path}")


def run_performance_tests(verbose=False):
    """Run performance tests."""
    command = ["python", "-m", "pytest", "tests/", "-m", "performance"]
    
    if verbose:
        command.append("-v")
    
    return run_command(command, "Performance Tests")


def run_security_tests(verbose=False):
    """Run security tests."""
    command = ["python", "-m", "pytest", "tests/", "-m", "security"]
    
    if verbose:
        command.append("-v")
    
    return run_command(command, "Security Tests")


def lint_code():
    """Run code linting."""
    commands = [
        (["python", "-m", "flake8", "platform/", "tests/"], "Flake8 Linting"),
        (["python", "-m", "black", "--check", "platform/", "tests/"], "Black Formatting Check"),
        (["python", "-m", "isort", "--check-only", "platform/", "tests/"], "Import Sorting Check"),
        (["python", "-m", "mypy", "platform/"], "Type Checking")
    ]
    
    results = []
    for command, description in commands:
        results.append(run_command(command, description))
    
    return all(results)


def format_code():
    """Format code using black and isort."""
    commands = [
        (["python", "-m", "black", "platform/", "tests/"], "Black Formatting"),
        (["python", "-m", "isort", "platform/", "tests/"], "Import Sorting")
    ]
    
    results = []
    for command, description in commands:
        results.append(run_command(command, description))
    
    return all(results)


def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        "pytest",
        "pytest-asyncio",
        "pytest-cov",
        "fastapi",
        "uvicorn",
        "requests",
        "websocket-client",
        "kivy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Install them with: pip install " + " ".join(missing_packages))
        return False
    else:
        print("✅ All required packages are installed")
        return True


def generate_test_report():
    """Generate a comprehensive test report."""
    command = [
        "python", "-m", "pytest", 
        "tests/", 
        "--html=test_report.html", 
        "--self-contained-html",
        "--cov=platform",
        "--cov-report=html:coverage_html",
        "--cov-report=term-missing",
        "-v"
    ]
    
    return run_command(command, "Test Report Generation")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="AI-AH Platform Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests
  python tests/run_tests.py --all

  # Run only unit tests
  python tests/run_tests.py --unit

  # Run tests with coverage
  python tests/run_tests.py --all --coverage

  # Run specific test file
  python tests/run_tests.py --test tests/test_agents.py

  # Run tests excluding slow tests
  python tests/run_tests.py --all --exclude-slow

  # Lint code
  python tests/run_tests.py --lint

  # Format code
  python tests/run_tests.py --format

  # Generate test report
  python tests/run_tests.py --report
        """
    )
    
    # Test selection options
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--agents", action="store_true", help="Run agent tests")
    parser.add_argument("--api", action="store_true", help="Run API tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--test", help="Run specific test file or function")
    
    # Test configuration options
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage")
    parser.add_argument("--exclude-slow", action="store_true", help="Exclude slow tests")
    
    # Code quality options
    parser.add_argument("--lint", action="store_true", help="Run code linting")
    parser.add_argument("--format", action="store_true", help="Format code")
    parser.add_argument("--check-deps", action="store_true", help="Check dependencies")
    
    # Report options
    parser.add_argument("--report", action="store_true", help="Generate test report")
    
    args = parser.parse_args()
    
    # Check dependencies first if requested
    if args.check_deps:
        if not check_dependencies():
            sys.exit(1)
        return
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    success = True
    
    # Run linting
    if args.lint:
        success &= lint_code()
    
    # Format code
    if args.format:
        success &= format_code()
    
    # Generate test report
    if args.report:
        success &= generate_test_report()
    
    # Run tests
    if args.all:
        success &= run_all_tests(args.verbose, args.coverage, args.exclude_slow)
    elif args.unit:
        success &= run_unit_tests(args.verbose, args.coverage)
    elif args.agents:
        success &= run_agent_tests(args.verbose, args.coverage)
    elif args.api:
        success &= run_api_tests(args.verbose, args.coverage)
    elif args.integration:
        success &= run_integration_tests(args.verbose, args.coverage)
    elif args.performance:
        success &= run_performance_tests(args.verbose)
    elif args.security:
        success &= run_security_tests(args.verbose)
    elif args.test:
        success &= run_specific_test(args.test, args.verbose)
    else:
        # Default: run all tests
        success &= run_all_tests(args.verbose, args.coverage, args.exclude_slow)
    
    # Print summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All operations completed successfully!")
    else:
        print("❌ Some operations failed. Check the output above for details.")
    print(f"{'='*60}")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
