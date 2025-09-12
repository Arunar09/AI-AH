# Tests

This directory contains all test files for the AI-AH platform.

## Structure

- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for component interactions
- `e2e/` - End-to-end tests for complete workflows
- `fixtures/` - Test data and fixtures

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run unit tests only
python -m pytest tests/unit/

# Run with coverage
python -m pytest tests/ --cov=ai_ah_platform
```

## Test Guidelines

1. Use descriptive test names
2. Follow AAA pattern (Arrange, Act, Assert)
3. Mock external dependencies
4. Keep tests independent
5. Use fixtures for common setup
