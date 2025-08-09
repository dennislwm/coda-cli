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

def test_import_template_cli_command():
  """TDD RED PHASE: Test import-template CLI command integration
  
  This test validates the CLI integration for the import-template command, which is 
  essential for making the import feature accessible to end users. Without CLI 
  integration, users would need to write Python code to use the import functionality, 
  which defeats the purpose of having a command-line tool. This test ensures that 
  users can import templates from the command line.
  
  RED PHASE: This will fail because import-template command doesn't exist in CLI yet.
  """
  runner = CliRunner()
  
  # Create a test YAML template file
  test_template = """
document:
  name: '{{DOC_NAME}}'
  sections:
  - name: Test Section
    type: canvas
    tables:
    - name: Test Table
      columns:
      - name: Test Column
        type: column
        format:
          type: text
"""
  
  with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
    temp_file.write(test_template)
    temp_filename = temp_file.name

  try:
    # Test Scenario 1: Basic import-template command with file
    # RED PHASE: This will fail because import-template command doesn't exist
    result = runner.invoke(clickMain, ['import-template', '--file', temp_filename])
    assert result.exit_code == 0
    assert "Document created successfully" in result.output
    # Should contain document ID in output
    assert "ID=" in result.output
    
    # Test Scenario 2: Import with variable substitution
    result = runner.invoke(clickMain, [
      'import-template', 
      '--file', temp_filename,
      '--variables', 'DOC_NAME="My CLI Test Project"'
    ])
    assert result.exit_code == 0
    assert "Document created successfully" in result.output
    assert "My CLI Test Project" in result.output
    
    # Test Scenario 3: Error handling - missing file
    result = runner.invoke(clickMain, ['import-template', '--file', 'nonexistent.yaml'])
    assert result.exit_code != 0
    assert "Error" in result.output
    
  finally:
    # Clean up temp file  
    if os.path.exists(temp_filename):
      os.unlink(temp_filename)


def test_register_template_cli_command():
  """TDD RED PHASE: Test register-template CLI command integration
  
  This test validates the CLI integration for the register-template command, which allows 
  users to register templates in the system's template registry for easy reuse. This 
  business behavior is essential for template management workflow where users can register 
  commonly used document structures and reference them by name later.
  
  RED PHASE: This will fail because register-template command doesn't exist in CLI yet.
  """
  runner = CliRunner()
  
  # Test Scenario 1: Register template with name and document ID
  # RED PHASE: This will fail because register-template command doesn't exist
  result = runner.invoke(clickMain, ['register-template', '--name', 'project-kickoff', '--doc', strTestDoc])
  assert result.exit_code == 0
  assert "Template 'project-kickoff' registered successfully" in result.output
  assert strTestDoc in result.output  # Should show the document ID in confirmation
  
  # Test Scenario 2: Register template with description
  result = runner.invoke(clickMain, [
    'register-template', 
    '--name', 'team-retrospective',
    '--doc', strDoc,
    '--description', 'Weekly team retrospective template'
  ])
  assert result.exit_code == 0
  assert "Template 'team-retrospective' registered successfully" in result.output
  assert "Weekly team retrospective template" in result.output
  
  # Test Scenario 3: Error handling - missing required arguments
  result = runner.invoke(clickMain, ['register-template', '--name', 'incomplete'])
  assert result.exit_code != 0
  assert "Error" in result.output or "Usage" in result.output
  
  # Test Scenario 4: Error handling - missing name argument
  result = runner.invoke(clickMain, ['register-template', '--doc', strDoc])
  assert result.exit_code != 0
  assert "Error" in result.output or "Usage" in result.output

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
  test_import_template_cli_command()
  test_register_template_cli_command()

if __name__ == "__main__":
  main()
