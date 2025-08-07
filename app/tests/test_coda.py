from coda import clickMain
from click.testing import CliRunner
import tempfile
import os

strDoc='QlIwnjdg3j'
strTable='table-6JxYP9k3MA'
# Test document ID specified by user for template export testing
strTestDoc='-vNHwSh0wi'

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

def test_export_template():
  """ Test export-template CLI command (TDD RED phase) """
  runner = CliRunner()
  
  # Test basic export-template command without output option
  result = runner.invoke(clickMain, ['export-template', '--doc', strTestDoc])
  assert result.exit_code == 0
  assert "document:" in result.output  # Should contain YAML with document key
  assert "name:" in result.output      # Should contain name key
  assert "sections:" in result.output  # Should contain sections key
  
  # Test export-template command with output file option
  with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
    temp_filename = temp_file.name
  
  try:
    result = runner.invoke(clickMain, ['export-template', '--doc', strTestDoc, '--output', temp_filename])
    assert result.exit_code == 0
    assert "Template exported to" in result.output or "exported" in result.output.lower()
    
    # Verify file was created and contains YAML content
    assert os.path.exists(temp_filename)
    with open(temp_filename, 'r') as f:
      content = f.read()
      assert "document:" in content
      assert "name:" in content
      assert "sections:" in content
  finally:
    # Clean up temp file
    if os.path.exists(temp_filename):
      os.unlink(temp_filename)

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
  test_export_template()

if __name__ == "__main__":
  main()
