from coda import clickMain
from click.testing import CliRunner
import json
import tempfile
import os
import pytest

strDoc = 'QlIwnjdg3j'
strTable = 'table-6JxYP9k3MA'
strTestDoc = '-vNHwSh0wi'
strSection = 'canvas-sVqFf3FEmk'
strColumn = 'c-7A8kI21s5R'

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
    (['get-doc', '--doc', strDoc], '"type": "doc"'),
    (['get-section', '--doc', strDoc, '--section', strSection], '"type": "page"'),
    (['get-column', '--doc', strDoc, '--table', strTable, '--column', strColumn], '"type": "column"'),
])
@pytest.mark.live
def test_basic_cli_commands(runner, command, expected_output):
    """Test basic CLI commands for successful execution and expected output patterns."""
    result = runner.invoke(clickMain, command)
    assert result.exit_code == 0
    if expected_output:
        assert expected_output in result.output

@pytest.mark.live
def test_export_template(runner, temp_yaml_file):
    # plumb:req-596d4d09
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

@pytest.mark.live
def test_import_template_cli_command(runner, temp_yaml_file):
    # plumb:req-4a71343a
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
    # plumb:req-795973cd
    # plumb:req-c38e6053
    # plumb:req-4371a5c9
    # plumb:req-b7b29744
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

@pytest.mark.live
def test_verify_auth(runner):
    """The verify-auth command confirms the configured API key is valid by calling the Coda /whoami endpoint."""
    result = runner.invoke(clickMain, ['verify-auth'])
    assert result.exit_code == 0
    data = json.loads(result.output.strip())
    assert "error" not in data
    assert any(k in data for k in ("loginId", "name", "type"))

def test_api_key_from_env_var(monkeypatch, tmp_path):
    """REQ-003: API key loads from CODA_API_KEY env var when no config.json is present."""
    from coda import Coda
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('CODA_API_KEY', 'test_env_key')
    obj = Coda('text')
    assert obj.API_KEY == 'test_env_key'

def test_api_key_from_config_file_overrides_env(monkeypatch, tmp_path):
    """REQ-003: config.json's CODA_API_KEY overrides the env var."""
    from coda import Coda
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('CODA_API_KEY', 'env_key')
    (tmp_path / 'config.json').write_text(json.dumps({'CODA_API_KEY': 'config_key'}))
    obj = Coda('text')
    assert obj.API_KEY == 'config_key'

def test_update_row_wraps_cells(monkeypatch):
    """REQ-009 regression: update_row must send codaio's {"row": {"cells": [...]}} shape, not a flat dict."""
    from common.pycoda import Pycoda
    obj = Pycoda('fake-key')
    captured = {}
    def fake_update_row(doc_id, table_id, row_id, data):
        captured['data'] = data
        return {"id": row_id}
    monkeypatch.setattr(obj.coda, 'update_row', fake_update_row)

    obj.update_row('doc1', 'table1', 'row1', {'c-abc': 'val'})

    assert captured['data'] == {"row": {"cells": [{"column": "c-abc", "value": "val"}]}}

def test_upsert_row_wraps_cells(monkeypatch):
    """REQ-009: upsert_row sends codaio's {"rows": [{"cells": [...]}], "keyColumns": [...]} shape."""
    from common.pycoda import Pycoda
    obj = Pycoda('fake-key')
    captured = {}
    def fake_upsert_row(doc_id, table_id, data):
        captured['data'] = data
        return {"requestId": "abc"}
    monkeypatch.setattr(obj.coda, 'upsert_row', fake_upsert_row)

    obj.upsert_row('doc1', 'table1', {'c-abc': 'val'}, lstKeyColumns=['c-abc'])

    assert captured['data'] == {
        "rows": [{"cells": [{"column": "c-abc", "value": "val"}]}],
        "keyColumns": ['c-abc'],
    }