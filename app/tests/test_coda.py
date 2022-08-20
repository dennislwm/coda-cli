from coda import clickMain
from click.testing import CliRunner

strDoc='QlIwnjdg3j'
strTable='table-6JxYP9k3MA'

def test_version():
  runner = CliRunner()
  result = runner.invoke(clickMain)
  assert result.exit_code == 0
  assert "v" in result.output 

def test_list_docs():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-docs'])
  assert result.exit_code == 0
  assert "doc" in result.output 

def test_list_controls():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-controls', '--doc', strDoc])
  assert result.exit_code == 0
  assert "control" in result.output 

def test_list_folders():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-folders', '--doc', strDoc])
  assert result.exit_code == 0
  # assert "folder" in result.output 

def test_list_formulas():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-formulas', '--doc', strDoc])
  assert result.exit_code == 0
  # assert "formula" in result.output 

def test_list_sections():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-sections', '--doc', strDoc])
  assert result.exit_code == 0
  assert "page" in result.output 

def test_list_tables():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-tables', '--doc', strDoc])
  assert result.exit_code == 0
  assert "table" in result.output 

def test_list_views():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-views', '--doc', strDoc])
  assert result.exit_code == 0
  assert "view" in result.output 

def test_list_columns():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-columns', '--doc', strDoc, '--table', strTable])
  assert result.exit_code == 0
  assert "col" in result.output 

def test_list_rows():
  runner = CliRunner()
  result = runner.invoke(clickMain, ['list-rows', '--doc', strDoc, '--table', strTable])
  assert result.exit_code == 0
  assert "row" in result.output 

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                M A I N   P R O C E D U R E                               |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
def main():
  test_version()
  test_list_docs()
  test_list_controls()
  test_list_folders()
  test_list_formulas()
  test_list_sections()
  test_list_tables()
  test_list_views()
  test_list_columns()
  test_list_rows()

if __name__ == "__main__":
  main()