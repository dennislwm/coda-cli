from coda import clickMain
from click.testing import CliRunner
import tempfile
import os
import pytest

strDoc = 'QlIwnjdg3j'
strTable = 'table-6JxYP9k3MA'
strTestDoc = '-vNHwSh0wi'

@pytest.fixture
def runner():
    """CLI runner fixture."""
    return CliRunner()

@pytest.fixture
def temp_yaml_file():
    """Temporary YAML template file fixture."""
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
    
    yield temp_filename
    
    if os.path.exists(temp_filename):
        os.unlink(temp_filename)

def _assert_yaml_structure(content):
    """Helper to validate YAML template structure."""
    required_keys = ["document:", "name:", "sections:"]
    assert all(key in content for key in required_keys)

@pytest.mark.parametrize("command,expected_output", [
    ([], "v"),
    (['list-docs'], "doc"),
    (['list-controls', '--doc', strDoc], "control"),
    (['list-folders', '--doc', strDoc], None),
    (['list-formulas', '--doc', strDoc], None),
    (['list-sections', '--doc', strDoc], "page"),
    (['list-tables', '--doc', strDoc], "table"),
    (['list-views', '--doc', strDoc], "view"),
    (['list-columns', '--doc', strDoc, '--table', strTable], "col"),
    (['list-rows', '--doc', strDoc, '--table', strTable], "row"),
])
def test_basic_cli_commands(runner, command, expected_output):
    """Test basic CLI commands for successful execution and expected output patterns."""
    result = runner.invoke(clickMain, command)
    assert result.exit_code == 0
    if expected_output:
        assert expected_output in result.output

def test_export_template(runner, temp_yaml_file):
    """Test export-template CLI command functionality."""
    # Test basic export without output file
    result = runner.invoke(clickMain, ['export-template', '--doc', strTestDoc])
    assert result.exit_code == 0
    _assert_yaml_structure(result.output)
    
    # Test export with output file
    result = runner.invoke(clickMain, ['export-template', '--doc', strTestDoc, '--output', temp_yaml_file])
    assert result.exit_code == 0
    assert "exported" in result.output.lower()
    
    assert os.path.exists(temp_yaml_file)
    with open(temp_yaml_file, 'r') as f:
        _assert_yaml_structure(f.read())

def test_import_template_cli_command(runner, temp_yaml_file):
    """Test import-template CLI functionality and error handling."""
    # Basic import functionality
    result = runner.invoke(clickMain, ['import-template', '--file', temp_yaml_file])
    assert result.exit_code == 0
    assert "Document created successfully" in result.output
    assert "ID=" in result.output
    
    # Import with variable substitution
    result = runner.invoke(clickMain, [
        'import-template', '--file', temp_yaml_file,
        '--variables', 'DOC_NAME="My CLI Test Project"'
    ])
    assert result.exit_code == 0
    assert "Document created successfully" in result.output
    assert "My CLI Test Project" in result.output
    
    # Error handling for missing file
    result = runner.invoke(clickMain, ['import-template', '--file', 'nonexistent.yaml'])
    assert result.exit_code != 0
    assert "Error" in result.output

def test_template_management_workflow(runner):
    """Test complete template registry workflow with error handling."""
    template_name = 'test-workflow-template'
    
    # Register template
    result = runner.invoke(clickMain, ['register-template', '--name', template_name, '--doc', strTestDoc])
    assert result.exit_code == 0
    assert f"Template '{template_name}' registered successfully" in result.output
    assert strTestDoc in result.output
    
    # Register with description
    desc_name = 'described-template'
    description = 'Test template with description'
    result = runner.invoke(clickMain, [
        'register-template', '--name', desc_name, '--doc', strDoc,
        '--description', description
    ])
    assert result.exit_code == 0
    assert f"Template '{desc_name}' registered successfully" in result.output
    assert description in result.output
    
    # List templates
    result = runner.invoke(clickMain, ['list-templates'])
    assert result.exit_code == 0
    assert "Registered Templates:" in result.output
    assert template_name in result.output
    assert strTestDoc in result.output
    
    # Remove template
    result = runner.invoke(clickMain, ['remove-template', '--name', template_name])
    assert result.exit_code == 0
    assert f"Template '{template_name}' removed successfully" in result.output
    
    # Verify removal
    result = runner.invoke(clickMain, ['list-templates'])
    assert result.exit_code == 0
    assert template_name not in result.output
    
    # Error handling cases
    result = runner.invoke(clickMain, ['remove-template', '--name', 'nonexistent-template'])
    assert result.exit_code == 0
    assert "Template 'nonexistent-template' not found in registry" in result.output
    
    # Test missing arguments
    for command in [
        ['register-template', '--name', 'incomplete'],
        ['register-template', '--doc', strDoc],
        ['remove-template']
    ]:
        result = runner.invoke(clickMain, command)
        assert result.exit_code != 0
        assert any(error_text in result.output for error_text in ["Error", "Usage"])

def test_list_templates_empty_registry(runner):
    """Test list-templates handles empty registry gracefully."""
    result = runner.invoke(clickMain, ['list-templates'])
    assert result.exit_code == 0
    assert any(text in result.output for text in ["No templates registered", "Registered Templates:"])