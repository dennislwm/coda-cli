# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
- `cd app` - Navigate to the application directory where all Python code lives
- `pipenv shell` - Activate the virtual environment
- `make install_new` - Install Python dependencies (click==8.1.3, codaio==0.6.10, pytest==6.2.4)

### Running the Application
- `python coda.py` - Run the CLI application
- `python coda.py --help` - Show available commands and options

### Testing
- `make test` - Run all tests using pytest
- `make test_verbose` - Run tests with verbose output
- `PYTHONPATH=. pytest` - Direct pytest execution

### Docker Operations
- `make docker_build` - Build Docker image locally
- `make docker_run` - Build and run Docker container with .env file
- `make ci_test_build` - Build Docker image for CI testing (includes test dependencies)

### Development Utilities
- `make install_freeze` - Generate requirements.txt from current dependencies
- `make shell_clean` - Remove the virtual environment

## Code Architecture

### Main Application Structure
- **app/coda.py**: Main CLI application using Click framework with command group structure
- **app/common/pycoda.py**: Wrapper around the codaio library for Coda.io API interactions
- **app/common/json_cli.py**: JSON utilities including JsonFile and JsonPlan classes

### CLI Command Pattern
The application follows a consistent pattern where:
1. Click commands are defined with decorators (`@clickMain.command()`)
2. Commands pass through to Coda class methods
3. Coda class delegates to Pycoda for API calls
4. Results are printed directly to stdout

### Configuration Management
- Environment variable: `CODA_API_KEY`
- JSON config file: `config.json` (overrides environment variable)
- Configuration is loaded in `Coda.load_config()` method

### Available Commands
- `list-docs` - List documents
- `list-sections`, `list-tables`, `list-controls`, `list-folders`, `list-formulas`, `list-views` - List document components
- `list-columns`, `list-rows` - List table components  
- `get-doc`, `get-section`, `get-column` - Get specific items

### Testing Structure
- Tests use Click's `CliRunner` for command-line testing
- Test files: `test_coda.py` (main functionality), `test_json.py` (JSON utilities)
- Tests require valid Coda document IDs for API testing

### Dependencies
- **codaio==0.6.10**: Third-party library for Coda.io API
- **click==8.1.3**: Command-line interface framework
- **pytest==6.2.4**: Testing framework

### Docker Configuration
- Multi-stage Python 3.10 based Dockerfile
- Requirements generated dynamically with pipreqs
- Environment variables passed via --env-file .env