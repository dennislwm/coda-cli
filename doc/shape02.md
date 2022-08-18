# Create test cases for each command with Python

<!-- TOC -->

- [Create test cases for each command with Python](#create-test-cases-for-each-command-with-python)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Test Driven Development](#test-driven-development)
- [Install developer dependencies](#install-developer-dependencies)
- [Create a test file](#create-a-test-file)

<!-- /TOC -->

# Constraint

Base time: 1 workday (Max: 2)

## Hill chart
```
 .
. +
0-1
```

# Place, Affordance, Connection

* Places users can navigate
  * Not applicable as tests are automated

* Affordance users can act
  * Test `python coda.py --version` returns exit code `0` and string containing `v`
  * Test `python coda.py list-docs` returns exit code `0` and json output containing `id`.

* Connection users are taken to
  * `python coda.py --version` --> `clickMain()` --> `Coda()` --> String --> Stdout
  * `python coda.py list-docs` --> `list_docs()` --> `Coda()` --> `objCoda.list_docs()` --> `pycoda.list_docs()` --> `codaio.list_docs()` --> Dict --> Json --> Stdout

# Test Driven Development

For this project, we're using both `pytest` and `click.testing` as our testing framework. 

# Install developer dependencies

1. Workstation

Before we can run our app, we need to activate virtual environment and install any dependencies. We use the flag `--dev` to specify that these packages are for development only.

```sh
cd app
pipenv shell
pipenv install --dev pytest==6.2.4
```

To uninstall any dependency.

```sh
pipenv uninstall pytest
```

To deactivate the virtual environment.

```sh
exit
```

2. Create a `make` command.

Edit the file `Makefile` and insert both targets `test` and `test_verbose` to the `.PHONY` declaration. Then add the following lines of code:

```makefile
test: 
	PYTHONPATH=.:../ pytest

test_verbose: 
	PYTHONPATH=.:../ pytest -v -s
```

# Create a test file

1. Create a `test` directory in the path `app/`. This is where we store our test files `test_*.py`, which will be auto-discoverable by `pytest`.

2. Create a file `test_coda.py` that holds all our test functions. Add the following lines of code:

```py
from coda import clickMain
from click.testing import CliRunner

def test_version():
  runner = CliRunner()
  result = runner.invoke(clickMain)
  assert result.exit_code == 0
  assert "v" in result.output 

def test_list_docs():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-docs'])
  assert result.exit_code == 0
  assert "id" in result.output 

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                M A I N   P R O C E D U R E                               |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
def main():
  test_version()
  test_list_docs()

if __name__ == "__main__":
  main()
```

3. Verify that our test works.

```sh
PYTHONPATH=.:$PWD pytest -v -s
```

```sh
===================================================== test session starts ======================================================
platform win32 -- Python 3.10.6, pytest-6.2.4, py-1.11.0, pluggy-0.13.1 -- C:\Users\I17271834\.virtualenvs\app-pPx9Rg3o\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\I17271834\Documents\home\coda-cli\app
collected 2 items

tests/test_coda.py::test_version PASSED
tests/test_coda.py::test_list_docs PASSED

====================================================== 2 passed in 0.54s =======================================================
```