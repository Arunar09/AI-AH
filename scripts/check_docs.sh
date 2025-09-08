#!/bin/bash
# Documentation completeness checker

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔍 Checking documentation...${NC}"

# Check for required files
required_files=(
    "README.md"
    "CONTEXT.md"
    "ARCHITECTURE.md"
    "PROJECT_GOVERNANCE.md"
    "docs/onboarding/CONTRIBUTING.md"
)

missing_files=0
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ Missing required file: $file${NC}"
        missing_files=$((missing_files + 1))
    else
        echo -e "${GREEN}✅ Found: $file${NC}"
    fi
done

# Check for TODOs in documentation
echo -e "\n${YELLOW}🔍 Checking for TODOs in documentation...${NC}"
todos=$(grep -r "TODO" docs/ *.md 2>/dev/null || true)
if [ -n "$todos" ]; then
    echo -e "${YELLOW}⚠️  Found TODOs in documentation:${NC}"
    echo "$todos" | while read -r line; do
        echo -e "  - $line"
    done
else
    echo -e "${GREEN}✅ No TODOs found in documentation${NC}"
fi

# Check for dead links
echo -e "\n${YELLOW}🔗 Checking for dead links...${NC}"
if ! command -v mdv &> /dev/null; then
    echo -e "${YELLOW}⚠️  markdown-link-check not installed, skipping link check${NC}"
    echo "Install with: npm install -g markdown-link-check"
else
    find . -name "*.md" -not -path "./venv/*" -not -path "./node_modules/*" | while read -r file; do
        echo "Checking links in $file"
        markdown-link-check -q "$file"
    done
fi

# Check documentation coverage
function check_coverage() {
    local dir=$1
    local pattern=$2
    local total=0
    local documented=0
    
    while IFS= read -r file; do
        total=$((total + 1))
        local doc_file="${file%.*}.md"
        if [ -f "$doc_file" ]; then
            documented=$((documented + 1))
        else
            echo -e "${YELLOW}⚠️  Missing documentation: $file${NC}"
        fi
    done < <(find "$dir" -name "$pattern" -not -path "*/__pycache__/*" -not -path "*/.git/*")
    
    if [ "$total" -gt 0 ]; then
        local coverage=$((documented * 100 / total))
        echo -e "\n${YELLOW}📊 Documentation Coverage: $coverage% ($documented/$total)${NC}"
        
        if [ "$coverage" -lt 80 ]; then
            echo -e "${RED}❌ Documentation coverage is below 80%${NC}"
            return 1
        fi
    fi
    
    return 0
}

echo -e "\n${YELLOW}📊 Checking code documentation...${NC}"
check_coverage "ai_ah" "*.py"

# Final status
if [ "$missing_files" -gt 0 ]; then
    echo -e "\n${RED}❌ $missing_files required files are missing${NC}"
    exit 1
else
    echo -e "\n${GREEN}✅ All documentation checks passed!${NC}"
fi
