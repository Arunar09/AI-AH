#!/usr/bin/env python3
"""
Project Health Monitor

This script generates metrics about project health, including:
- Documentation coverage
- Test coverage
- Open issues/PRs
- Code quality metrics
"""
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class ProjectHealthMonitor:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.metrics: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': {}
        }
    
    def collect_metrics(self):
        """Collect all project health metrics."""
        self._collect_documentation_metrics()
        self._collect_test_metrics()
        self._collect_code_metrics()
        self._collect_issue_metrics()
        return self.metrics
    
    def _collect_documentation_metrics(self):
        """Collect documentation coverage metrics."""
        doc_files = list(self.root.glob('**/*.md'))
        code_files = list(self.root.glob('**/*.py'))
        
        self.metrics['metrics']['documentation'] = {
            'doc_file_count': len(doc_files),
            'code_file_count': len(code_files),
            'doc_to_code_ratio': len(doc_files) / max(len(code_files), 1),
            'undocumented_files': self._find_undocumented_files()
        }
    
    def _collect_test_metrics(self):
        """Collect test coverage metrics."""
        try:
            result = subprocess.run(
                ['pytest', '--cov=ai_ah', '--cov-report=json'],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            coverage_data = json.loads(result.stdout)
            
            self.metrics['metrics']['test_coverage'] = {
                'line_coverage': coverage_data['totals']['percent_covered'],
                'total_lines': coverage_data['totals']['covered_lines'] + coverage_data['totals']['missing_lines'],
                'covered_lines': coverage_data['totals']['covered_lines']
            }
        except Exception as e:
            self.metrics['metrics']['test_coverage'] = {
                'error': str(e)
            }
    
    def _collect_code_metrics(self):
        """Collect code quality metrics."""
        try:
            # Run flake8 for code quality
            flake8 = subprocess.run(
                ['flake8', '--count', '--max-complexity=10', '--max-line-length=88', 'ai_ah/'],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            
            # Count lines of code
            cloc = subprocess.run(
                ['cloc', '--json', 'ai_ah/'],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            
            self.metrics['metrics']['code_quality'] = {
                'flake8_issues': int(flake8.stdout.strip() or '0'),
                'lines_of_code': json.loads(cloc.stdout)['SUM']['code'] if cloc.returncode == 0 else None
            }
        except Exception as e:
            self.metrics['metrics']['code_quality'] = {
                'error': str(e)
            }
    
    def _collect_issue_metrics(self):
        """Collect issue and PR metrics."""
        try:
            # This would be replaced with actual GitHub API calls in a real implementation
            self.metrics['metrics']['issues'] = {
                'open_issues': 0,  # Placeholder
                'open_prs': 0,     # Placeholder
                'avg_time_to_close': None
            }
        except Exception as e:
            self.metrics['metrics']['issues'] = {
                'error': str(e)
            }
    
    def _find_undocumented_files(self) -> list:
        """Find Python files missing documentation."""
        undocumented = []
        for py_file in self.root.glob('ai_ah/**/*.py'):
            if py_file.name == '__init__.py':
                continue
                
            doc_file = py_file.with_suffix('.md')
            if not doc_file.exists():
                undocumented.append(str(py_file.relative_to(self.root)))
        
        return undocumented
    
    def generate_report(self) -> str:
        """Generate a human-readable report."""
        report = [
            "📊 Project Health Report",
            f"Generated at: {self.metrics['timestamp']}\n"
        ]
        
        # Documentation
        doc = self.metrics['metrics']['documentation']
        report.extend([
            "📚 Documentation",
            f"- Files: {doc['doc_file_count']} documentation files",
            f"- Code to Doc Ratio: {doc['doc_to_code_ratio']:.2f} (docs per code file)",
            f"- Undocumented Files: {len(doc['undocumented_files'])}"
        ])
        
        # Test Coverage
        if 'test_coverage' in self.metrics['metrics']:
            cov = self.metrics['metrics']['test_coverage']
            if 'error' not in cov:
                report.extend([
                    "\n✅ Test Coverage",
                    f"- Line Coverage: {cov['line_coverage']:.1f}%",
                    f"- Lines Covered: {cov['covered_lines']}/{cov['total_lines']}"
                ])
            else:
                report.append(f"\n❌ Test Coverage Error: {cov['error']}")
        
        # Code Quality
        if 'code_quality' in self.metrics['metrics']:
            qual = self.metrics['metrics']['code_quality']
            if 'error' not in qual:
                report.extend([
                    "\n🔍 Code Quality",
                    f"- Flake8 Issues: {qual['flake8_issues']}",
                    f"- Lines of Code: {qual['lines_of_code'] or 'N/A'}"
                ])
            else:
                report.append(f"\n❌ Code Quality Error: {qual['error']}")
        
        return '\n'.join(report)

def main():
    monitor = ProjectHealthMonitor()
    metrics = monitor.collect_metrics()
    
    # Print report
    print(monitor.generate_report())
    
    # Save metrics
    metrics_file = monitor.root / 'metrics' / 'project_health.json'
    metrics_file.parent.mkdir(exist_ok=True)
    
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n✅ Metrics saved to {metrics_file.relative_to(monitor.root)}")

if __name__ == "__main__":
    main()
