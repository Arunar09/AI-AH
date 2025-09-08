# Cleanup script for AI-AH project
Write-Host "Starting cleanup..." -ForegroundColor Green

# 1. Remove Python cache files
Write-Host "[1/7] Removing Python cache files..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include "__pycache__" -Recurse -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Include "*.pyc", "*.pyo", "*.pyd" -Recurse -File | Remove-Item -Force -ErrorAction SilentlyContinue

# 2. Remove logs and databases
Write-Host "[2/7] Removing log files and databases..." -ForegroundColor Yellow
Remove-Item -Path ".\ai_ah.log" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\base_agent.db" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\tests\base_agent.db" -Force -ErrorAction SilentlyContinue

# 3. Clean workspace and old test directories
Write-Host "[3/7] Cleaning workspaces and old test directories..." -ForegroundColor Yellow
# Clean main workspace
if (Test-Path ".\workspace") {
    Remove-Item -Path ".\workspace\*" -Recurse -Force -ErrorAction SilentlyContinue
}
# Remove old test workspaces
Remove-Item -Path ".\web_terraform_workspace" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\tests\web_terraform_workspace" -Recurse -Force -ErrorAction SilentlyContinue

# 4. Clean Terraform cache and state
Write-Host "[4/7] Cleaning Terraform cache and state..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include ".terraform" -Recurse -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Include ".terraform.lock.hcl", "*.tfstate*" -Recurse -File | Remove-Item -Force -ErrorAction SilentlyContinue

# 5. Clean old versioned files
Write-Host "[5/7] Removing old versioned files..." -ForegroundColor Yellow
# Old capability files
Remove-Item -Path ".\results\AGENT_CAPABILITIES_v1.*.md" -Force -ErrorAction SilentlyContinue
# Old test results
Remove-Item -Path ".\results\agent_test_results_v*.json" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\tests\agent_test_results_v*.json" -Force -ErrorAction SilentlyContinue
# Old test files
Remove-Item -Path ".\tests\agent_50_scale_test.py" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\tests\agent_capability_test*.py" -Force -ErrorAction SilentlyContinue

# 6. Clean old core files
Write-Host "[6/7] Cleaning old core files..." -ForegroundColor Yellow
Remove-Item -Path ".\core\example_docker_plugin.py" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\core\terraform_plugin.py" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\core\terraform_engineer_plugin.py" -Force -ErrorAction SilentlyContinue

# 7. Clean test coverage reports
Write-Host "[7/7] Cleaning test coverage reports..." -ForegroundColor Yellow
Remove-Item -Path ".\.coverage" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\.pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\htmlcov" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "`nCleanup complete! The following items were cleaned:" -ForegroundColor Green
Write-Host "- Python cache files (*.pyc, __pycache__)"
Write-Host "- Log and database files"
Write-Host "- Workspace and test directories"
Write-Host "- Terraform cache and state files"
Write-Host "- Old versioned files and test results"
Write-Host "- Old core plugin files"
Write-Host "- Test coverage reports`n"

Write-Host "Note: The following documentation files were not removed but may need review:"
Write-Host "- PROJECT_DEVELOPER_GUIDE.md"
Write-Host "- PROJECT_GOVERNANCE.md"
Write-Host "- IMPLEMENTATION_PLAN.md`n"

Write-Host "Run 'git status' to see the changes and 'git add .' to stage them." -ForegroundColor Cyan
