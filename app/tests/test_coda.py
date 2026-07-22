from coda import clickMain
from click.testing import CliRunner
from unittest.mock import patch
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

def test_import_template_cli_command(runner, temp_yaml_file):
    # plumb:req-4a71343a
    """Test import-template CLI functionality and error handling."""
    with patch('common.pycoda.Pycoda.create_document') as mock_create:
        # Basic import functionality
        mock_create.return_value = json.dumps({"id": "doc-abc123", "name": "{{DOC_NAME}}"})
        result = runner.invoke(clickMain, ['import-template', '--file', temp_yaml_file])
        assert result.exit_code == 0
        assert "Document created successfully" in result.output
        assert "ID=" in result.output

        # Import with variable substitution
        mock_create.return_value = json.dumps({"id": "doc-def456", "name": "My CLI Test Project"})
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

def test_sync(runner):
    """REQ-013: sync command upserts docs/tables into the registry and prunes stale entries"""
    with patch('coda.TemplateRegistry') as mock_registry_class, \
         patch('common.pycoda.Pycoda.list_docs_raw') as mock_docs, \
         patch('common.pycoda.Pycoda.list_tables_raw') as mock_tables:

        mock_registry = mock_registry_class.return_value
        mock_docs.return_value = [{"id": "doc-1", "name": "MyDoc"}]
        mock_tables.return_value = [{"id": "table-1", "name": "MyTable"}]
        mock_registry.prune_synced.return_value = 2

        result = runner.invoke(clickMain, ['sync'])

        assert result.exit_code == 0
        mock_registry.register_doc.assert_called_once_with("MyDoc", "doc-1", {"MyTable": "table-1"})
        mock_registry.prune_synced.assert_called_once_with({"MyDoc"})
        assert "Synced 1 docs, pruned 2 stale" in result.output

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

@pytest.mark.parametrize('command,extra', [
    ('update-row', ['--row', 'i-abc123', '--cells', 'c-abc=val']),
    ('upsert-row', ['--cells', 'c-abc=val']),
])
def test_write_path_fails_on_api_error(runner, command, extra):
    """REQ-020: an {"error": ...} from a write must exit non-zero, not print as success."""
    method = command.replace('-', '_')
    with patch('common.template_registry.TemplateRegistry') as mock_registry_class, \
         patch(f'common.pycoda.Pycoda.{method}') as mock_write:

        mock_registry = mock_registry_class.return_value
        mock_registry.get_table_id.return_value = 'grid-abc123'
        mock_registry.get_template_doc_id.return_value = '-vNHwSh0wi'
        mock_registry.is_template_registered.return_value = True
        mock_write.return_value = json.dumps({"error": "401 Unauthorized"})

        result = runner.invoke(clickMain, [
            command, '--doc', 'PokemonLeesarebest', '--table', 'Cards',
        ] + extra)

        assert result.exit_code != 0
        assert "401 Unauthorized" in result.output

@pytest.mark.parametrize('command,extra', [
    ('update-row', ['--row', 'i-abc123', '--cells', 'c-abc=val']),
    ('upsert-row', ['--cells', 'c-abc=val']),
    ('get-column', ['--column', 'c-abc']),
])
def test_write_path_resolves_table_name(runner, command, extra):
    """REQ-019: every --table command must resolve the name like list_rows does (ADR-06)."""
    method = command.replace('-', '_')
    with patch('common.template_registry.TemplateRegistry') as mock_registry_class, \
         patch(f'common.pycoda.Pycoda.{method}') as mock_write:

        mock_registry = mock_registry_class.return_value
        mock_registry.get_table_id.return_value = 'grid-abc123'
        mock_registry.get_template_doc_id.return_value = '-vNHwSh0wi'
        mock_registry.is_template_registered.return_value = True
        mock_write.return_value = {"id": "i-abc123"}

        result = runner.invoke(clickMain, [
            command, '--doc', 'PokemonLeesarebest', '--table', 'Cards',
        ] + extra)

        assert result.exit_code == 0
        mock_registry.get_table_id.assert_called_once_with('PokemonLeesarebest', 'Cards')
        assert mock_write.call_args[0][:2] == ('-vNHwSh0wi', 'grid-abc123')