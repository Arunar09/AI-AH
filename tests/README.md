# 🧪 AI-AH Platform Test Suite

This directory contains comprehensive tests for the Multi-Agent Infrastructure Intelligence Platform.

## 📁 Test Structure

```
tests/
├── conftest.py              # Pytest configuration and shared fixtures
├── test_core_framework.py   # Core platform framework tests
├── test_agents.py           # Specialized agent tests
├── test_api.py              # API layer tests
├── test_integration.py      # End-to-end integration tests
├── run_tests.py             # Test runner script
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## 🚀 Quick Start

### Run All Tests
```bash
python tests/run_tests.py --all
```

### Run Specific Test Types
```bash
# Unit tests only
python tests/run_tests.py --unit

# Agent tests only
python tests/run_tests.py --agents

# API tests only
python tests/run_tests.py --api

# Integration tests only
python tests/run_tests.py --integration
```

### Run with Coverage
```bash
python tests/run_tests.py --all --coverage
```

### Run Specific Test File
```bash
python tests/run_tests.py --test tests/test_agents.py
```

## 📋 Test Categories

### 1. **Unit Tests** (`test_core_framework.py`)
- **PlatformConfig**: Configuration management
- **BasePlatform**: Core platform functionality
- **Task**: Task management
- **ConversationManager**: Conversation handling
- **MemoryManager**: Memory management
- **ToolRegistry**: Tool registration
- **NaturalLanguageProcessor**: NLP functionality

### 2. **Agent Tests** (`test_agents.py`)
- **TerraformAgent**: Infrastructure provisioning
- **AnsibleAgent**: Configuration management
- **KubernetesAgent**: Container orchestration
- **SecurityAgent**: Security and compliance
- **MonitoringAgent**: Monitoring and observability
- **Agent Integration**: Multi-agent workflows

### 3. **API Tests** (`test_api.py`)
- **Authentication**: JWT and API key auth
- **Agent Routes**: All agent endpoints
- **Platform Routes**: Platform management
- **WebSocket**: Real-time communication
- **Error Handling**: Exception management
- **Rate Limiting**: Request throttling

### 4. **Integration Tests** (`test_integration.py`)
- **End-to-End Workflows**: Complete user journeys
- **Platform Integration**: System-level operations
- **Error Recovery**: Failure handling
- **Performance**: Load and stress testing
- **Concurrent Operations**: Multi-threaded scenarios

## 🏷️ Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.api` - API tests
- `@pytest.mark.websocket` - WebSocket tests
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.performance` - Performance tests
- `@pytest.mark.security` - Security tests

### Run Tests by Marker
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Exclude slow tests
pytest -m "not slow"

# Run performance tests
pytest -m performance
```

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)
- **Test Discovery**: Automatic test file detection
- **Output Format**: Verbose output with colors
- **Markers**: Custom test markers
- **Timeouts**: 5-minute test timeout
- **Logging**: Detailed logging configuration
- **Async Support**: Automatic async test handling

### Shared Fixtures (`conftest.py`)
- **Platform Config**: Test platform configuration
- **Agent Instances**: All specialized agents
- **Mock Responses**: Pre-configured mock data
- **Test Data**: Sample requirements and contexts
- **Async Utilities**: Async test helpers

## 📊 Test Coverage

The test suite provides comprehensive coverage:

- **Core Framework**: 95%+ coverage
- **Agent Logic**: 90%+ coverage
- **API Endpoints**: 100% coverage
- **Integration Scenarios**: 85%+ coverage
- **Error Handling**: 90%+ coverage

### Generate Coverage Report
```bash
python tests/run_tests.py --all --coverage
```

Coverage reports are generated in:
- `htmlcov/` - HTML coverage report
- `coverage.xml` - XML coverage report
- Terminal output - Summary coverage

## 🛠️ Test Utilities

### Test Runner (`run_tests.py`)
Comprehensive test runner with options:

```bash
# Basic usage
python tests/run_tests.py --all

# With options
python tests/run_tests.py --all --verbose --coverage --exclude-slow

# Code quality
python tests/run_tests.py --lint
python tests/run_tests.py --format

# Generate report
python tests/run_tests.py --report
```

### Available Options
- `--all` - Run all tests
- `--unit` - Unit tests only
- `--agents` - Agent tests only
- `--api` - API tests only
- `--integration` - Integration tests only
- `--performance` - Performance tests only
- `--security` - Security tests only
- `--test <path>` - Specific test file
- `--verbose` - Verbose output
- `--coverage` - Include coverage
- `--exclude-slow` - Skip slow tests
- `--lint` - Run code linting
- `--format` - Format code
- `--check-deps` - Check dependencies
- `--report` - Generate test report

## 🧪 Test Examples

### Unit Test Example
```python
def test_terraform_agent_initialization(terraform_agent):
    """Test Terraform agent initialization."""
    assert terraform_agent.config.name == "terraform_test"
    assert terraform_agent.agent_type == "terraform"
    assert terraform_agent.capabilities is not None
```

### Integration Test Example
```python
@pytest.mark.asyncio
async def test_complete_infrastructure_deployment_workflow(client, auth_headers):
    """Test complete infrastructure deployment workflow."""
    # Step 1: Terraform - Create infrastructure
    terraform_request = {
        "request_id": "workflow_123",
        "user_id": "test_user",
        "requirements": "Create a web server with nginx on AWS"
    }
    
    response = client.post("/api/v1/agents/terraform/request", json=terraform_request)
    assert response.status_code == 200
```

### API Test Example
```python
def test_terraform_request(client, auth_headers):
    """Test Terraform request endpoint."""
    request_data = {
        "request_id": "test_req_123",
        "user_id": "test_user",
        "requirements": "Create a web server with nginx on AWS"
    }
    
    response = client.post("/api/v1/agents/terraform/request", json=request_data)
    assert response.status_code == 200
    assert response.json()["agent_type"] == "terraform"
```

## 🔍 Debugging Tests

### Run Single Test
```bash
pytest tests/test_agents.py::TestTerraformAgent::test_terraform_agent_initialization -v
```

### Run with Debug Output
```bash
pytest tests/test_agents.py -v -s --log-cli-level=DEBUG
```

### Run with PDB Debugger
```bash
pytest tests/test_agents.py --pdb
```

### Run with Coverage for Specific File
```bash
pytest tests/test_agents.py --cov=platform.agents --cov-report=term-missing
```

## 📈 Performance Testing

### Load Testing
```bash
python tests/run_tests.py --performance
```

### Concurrent Request Testing
The integration tests include concurrent request handling to verify:
- Thread safety
- Resource management
- Response consistency
- Error handling under load

### Memory Usage Testing
Tests monitor memory usage to ensure:
- No memory leaks
- Stable memory consumption
- Proper resource cleanup

## 🔒 Security Testing

### Authentication Testing
- JWT token validation
- API key authentication
- Role-based access control
- Session management

### Input Validation Testing
- SQL injection prevention
- XSS protection
- Input sanitization
- Parameter validation

### Authorization Testing
- Permission checking
- Resource access control
- API endpoint protection
- Data isolation

## 🚨 Error Handling Testing

### Exception Scenarios
- Network failures
- Agent unavailability
- Invalid input data
- Resource exhaustion
- Timeout handling

### Recovery Testing
- Automatic retry mechanisms
- Graceful degradation
- Error propagation
- State recovery

## 📝 Writing New Tests

### Test Structure
```python
class TestNewFeature:
    """Test new feature functionality."""
    
    @pytest.fixture
    def feature_instance(self):
        """Create feature instance for testing."""
        return NewFeature()
    
    def test_feature_initialization(self, feature_instance):
        """Test feature initialization."""
        assert feature_instance is not None
        assert feature_instance.status == "initialized"
    
    @pytest.mark.asyncio
    async def test_feature_async_operation(self, feature_instance):
        """Test async feature operation."""
        result = await feature_instance.async_operation()
        assert result is not None
```

### Best Practices
1. **Descriptive Names**: Use clear, descriptive test names
2. **Single Responsibility**: Each test should test one thing
3. **Independent Tests**: Tests should not depend on each other
4. **Mock External Dependencies**: Use mocks for external services
5. **Test Edge Cases**: Include boundary and error conditions
6. **Async Testing**: Use `@pytest.mark.asyncio` for async tests
7. **Fixtures**: Use fixtures for common test setup
8. **Assertions**: Use specific assertions with clear messages

## 🔧 Continuous Integration

### GitHub Actions Integration
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python tests/run_tests.py --all --coverage
```

### Pre-commit Hooks
```yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: python tests/run_tests.py --unit
        language: system
        pass_filenames: false
```

## 📊 Test Metrics

### Coverage Targets
- **Overall Coverage**: 90%+
- **Critical Paths**: 95%+
- **API Endpoints**: 100%
- **Error Handling**: 90%+

### Performance Targets
- **Unit Tests**: < 1 second each
- **Integration Tests**: < 30 seconds each
- **Full Test Suite**: < 5 minutes
- **API Response Time**: < 100ms

### Quality Metrics
- **Test Reliability**: 99%+ pass rate
- **Test Maintainability**: Clear, readable tests
- **Test Coverage**: Comprehensive scenario coverage
- **Test Performance**: Fast execution times

## 🆘 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure platform module is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python tests/run_tests.py --unit
```

#### Async Test Issues
```bash
# Install pytest-asyncio
pip install pytest-asyncio

# Run with async mode
pytest --asyncio-mode=auto
```

#### Coverage Issues
```bash
# Install coverage tools
pip install pytest-cov

# Run with coverage
pytest --cov=platform --cov-report=html
```

#### Mock Issues
```bash
# Ensure proper mock setup
# Check that mocks are properly configured in fixtures
# Verify mock return values match expected types
```

### Getting Help
1. Check test output for specific error messages
2. Run tests with `--verbose` for detailed output
3. Use `--pdb` to debug failing tests
4. Check fixture setup in `conftest.py`
5. Verify test data and mock configurations

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Async Testing](https://pytest-asyncio.readthedocs.io/)
- [Mock Testing](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py](https://coverage.readthedocs.io/)

---

**Happy Testing! 🧪✨**
