# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Playwright + pytest automation testing framework for CliniqNexus, supporting API, UI, and end-to-end testing. The project uses Python with Playwright for browser automation and pytest as the test runner.

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
./activate.sh
# or manually
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test types
pytest tests/ui/           # UI tests
pytest tests/api/          # API tests
pytest tests/e2e/          # End-to-end tests

# Run specific test file
pytest tests/ui/test_login_page.py

# Run with Playwright
playwright test

# Run with specific environment
TEST_ENV=test pytest tests/ui/test_login_page.py
BASE_URL=http://62.234.96.153:55409 pytest tests/ui/
```

### Test Configuration
- Default test environment: `test` (http://62.234.96.153:55409)
- Default browser: `chromium`
- Headless mode: `false` by default (visible browser)
- Test timeout: 300 seconds

### Debugging and Reporting
```bash
# Run with visible browser
HEADLESS=false pytest tests/ui/test_login_page.py

# Verbose output with detailed traceback
pytest -v -s --tb=long

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Generate JSON report
pytest --json-report --json-report-file=reports/report.json
```

## Architecture

### Test Organization
- **tests/ui/**: UI tests using Playwright page objects
- **tests/api/**: API tests using requests
- **tests/e2e/**: End-to-end workflow tests

### Page Object Pattern
- **pages/**: Page object classes following Playwright POM pattern
- Each page class inherits from `BasePage`
- Page objects handle element locators and interaction methods

### Configuration System
- **config/environments.py**: Multi-environment configuration (dev/test/staging/production)
- **config/settings.py**: Global project settings and constants
- Environment selection via `TEST_ENV` environment variable

### Utilities
- **utils/browser_manager.py**: Browser lifecycle management
- **utils/data_helper.py**: Test data loading (JSON/YAML)
- **utils/screenshot_helper.py**: Screenshot capture on test failure

### Fixtures (conftest.py)
- `browser_manager`: Session-level browser management
- `page`: Function-level page instance
- `screenshot_helper`: Automatic screenshot capture
- `test_data`/`user_data`: Test data loading

## Key Configuration Files

### pytest.ini
- Test discovery patterns
- Default pytest options (verbose, short traceback, HTML/JSON reporting)
- Custom markers (smoke, regression, api, ui, e2e, slow, skip)

### playwright.config.js
- Browser configuration (Chromium, Firefox, WebKit, mobile)
- Test timeout and retry settings
- Report generation (HTML, JSON, JUnit)
- Base URL configuration with environment support

### Environment Configuration
- Test environment: `http://62.234.96.153:55409`
- Default user: `lovely_hu@qq.com` / `test123456`
- Environment switching via `TEST_ENV` or `BASE_URL`

## Development Workflow

### Adding New Tests
1. Create page object in `pages/` directory
2. Write test in appropriate `tests/` subdirectory
3. Use existing fixtures from `conftest.py`
4. Follow page object pattern for UI tests

### Environment Management
- Use `TEST_ENV=test` for test environment
- Use `BASE_URL` to override specific URLs
- Configuration loaded from `config/environments.py`

### Test Data
- User credentials in `data/users.yaml`
- General test data in `data/test_data.json`
- Data loaded via `DataHelper` utility class

## Important Notes

- Tests run against a live test environment at `http://62.234.96.153:55409`
- Screenshots automatically captured on test failure in `screenshots/`
- Reports generated in `reports/` directory
- Project uses Git Flow branching strategy (main/develop/feature branches)