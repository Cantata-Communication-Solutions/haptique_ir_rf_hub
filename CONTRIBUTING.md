# Contributing to Haptique IR/RF Hub Integration

## For Official Home Assistant Integration

### Quality Checklist

Before submitting to Home Assistant core:

- [ ] All code follows [Home Assistant Code Style](https://developers.home-assistant.io/docs/development_guidelines/)
- [ ] `manifest.json` is properly configured
- [ ] Config flow implemented (UI configuration)
- [ ] `strings.json` with proper translations
- [ ] All code has type hints
- [ ] Tests written with >90% coverage
- [ ] Passes `pylint` and `black` checks
- [ ] Documentation complete
- [ ] No blocking calls in event loop
- [ ] Follows Home Assistant architecture patterns

### Development Setup
```bash
# Clone repository
git clone https://github.com/Cantata-Communication-Solutions/haptique_ir_rf_hub.git
cd haptique_ir_rf_hub

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_test.txt

# Run tests
pytest

# Run type checking
mypy custom_components/haptique_ir_rf_hub

# Check code style
black custom_components/haptique_ir_rf_hub
pylint custom_components/haptique_ir_rf_hub
```

### Testing
```bash
# Run all tests with coverage
pytest --cov

# Run specific test file
pytest tests/test_config_flow.py

# Run with verbose output
pytest -v
```

### Code Quality

This integration follows Home Assistant's quality standards:

- **Type Hints**: All functions must have type hints
- **Docstrings**: All public functions need docstrings
- **Async**: Use async/await properly
- **No Blocking**: No blocking I/O in event loop
- **Logging**: Use proper logging levels
- **Constants**: Use const.py for all constants

### Submitting Changes

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Ensure all tests pass
5. Submit pull request

For submission to Home Assistant core repository, see:
https://developers.home-assistant.io/docs/creating_integration_manifest
