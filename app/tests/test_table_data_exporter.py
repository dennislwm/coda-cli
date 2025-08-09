from coda import clickMain
from click.testing import CliRunner
import tempfile
import os
import json
from unittest.mock import patch


def test_export_table_basic():
    """Test basic CSV export functionality
    
    This test validates the core business requirement: export table data as CSV via CLI.
    Now we mock the API responses to provide predictable test data.
    """
    # Mock API responses with expected data structure
    mock_columns = [
        {"name": "Name", "type": "text"},
        {"name": "Status", "type": "select"},
        {"name": "Date", "type": "date"}
    ]
    
    mock_rows = [
        {"values": {"Name": "Task 1", "Status": "Active", "Date": "2024-01-01"}}
    ]
    
    with patch('common.pycoda.Pycoda.list_columns') as mock_list_columns, \
         patch('common.pycoda.Pycoda.list_rows') as mock_list_rows:
        
        mock_list_columns.return_value = json.dumps(mock_columns)
        mock_list_rows.return_value = json.dumps(mock_rows)
        
        runner = CliRunner()
        result = runner.invoke(clickMain, [
            'export-table', '--doc', 'test-doc-id', '--table', 'test-table-id'
        ])
        
        assert result.exit_code == 0
        assert 'Name,Status,Date' in result.output  # Expected CSV headers
        assert 'Task 1,Active,2024-01-01' in result.output  # Expected CSV data


def test_export_table_invalid_ids():
    """Test error handling for invalid document/table IDs
    
    This test ensures that invalid IDs result in meaningful error messages
    rather than cryptic API errors or crashes.
    """
    # Mock API to raise an exception for invalid IDs
    with patch('common.pycoda.Pycoda.list_columns') as mock_list_columns:
        # Simulate API error for invalid document ID
        mock_list_columns.side_effect = Exception("Document not found")
        
        runner = CliRunner()
        result = runner.invoke(clickMain, [
            'export-table', '--doc', 'invalid-doc-id', '--table', 'valid-table-id'
        ])
        
        assert result.exit_code != 0  # Should fail
        assert "error" in result.output.lower()  # Should contain error message
        assert "export failed" in result.output.lower()  # Should be user-friendly


def test_export_table_file_permission_error():
    """Test error handling for file permission errors
    
    This test ensures that file permission issues are handled gracefully
    with clear error messages for users.
    """
    # Mock successful API calls
    mock_columns = [{"name": "Task", "type": "text"}]
    mock_rows = [{"values": {"Task": "Test task"}}]
    
    with patch('common.pycoda.Pycoda.list_columns') as mock_list_columns, \
         patch('common.pycoda.Pycoda.list_rows') as mock_list_rows, \
         patch('builtins.open', side_effect=PermissionError("Permission denied")):
        
        mock_list_columns.return_value = json.dumps(mock_columns)
        mock_list_rows.return_value = json.dumps(mock_rows)
        
        runner = CliRunner()
        result = runner.invoke(clickMain, [
            'export-table', '--doc', 'test-doc', '--table', 'test-table',
            '--output', '/readonly/path/output.csv'
        ])
        
        assert result.exit_code != 0  # Should fail
        # Click exceptions appear in result.exception, not result.output
        error_text = str(result.exception).lower() if result.exception else result.output.lower()
        assert "permission denied" in error_text  # Should mention permission issue


def test_export_to_file_and_unicode():
    """Test file output functionality and Unicode character handling
    
    This test ensures that:
    1. The --output flag correctly writes CSV to a file
    2. Unicode characters in table data are properly handled
    3. The file contains the expected CSV structure and can be read back
    """
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        temp_file = tmp.name
    
    try:
        # Mock Unicode data to test international character support
        unicode_columns = [
            {"name": "项目", "type": "text"},      # Project (Chinese)
            {"name": "状态", "type": "select"},    # Status (Chinese) 
            {"name": "Müller", "type": "person"}  # German name with umlaut
        ]
        
        unicode_rows = [
            {"values": {"项目": "测试项目", "状态": "进行中", "Müller": "José García"}},  # Mixed languages
            {"values": {"项目": "Production", "状态": "完成", "Müller": "François"}}
        ]
        
        with patch('common.pycoda.Pycoda.list_columns') as mock_list_columns, \
             patch('common.pycoda.Pycoda.list_rows') as mock_list_rows:
            
            mock_list_columns.return_value = json.dumps(unicode_columns)
            mock_list_rows.return_value = json.dumps(unicode_rows)
            
            runner = CliRunner()
            result = runner.invoke(clickMain, [
                'export-table', '--doc', 'test-doc', '--table', 'test-table',
                '--output', temp_file
            ])
            
            # Should succeed
            assert result.exit_code == 0
            assert "exported to" in result.output.lower()
            
            # Verify file was created
            assert os.path.exists(temp_file)
            
            # Verify file content with proper UTF-8 encoding
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Should contain Unicode headers
                assert "项目,状态,Müller" in content
                
                # Should contain Unicode data 
                assert "测试项目,进行中,José García" in content
                assert "Production,完成,François" in content
                
                # Verify proper CSV structure
                lines = content.strip().split('\n')
                assert len(lines) == 3  # Header + 2 data rows
                
                # Verify each line has correct number of fields
                for line in lines:
                    fields = line.split(',')
                    assert len(fields) == 3  # 3 columns
                    
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_export_csv_special_characters():
    """Test CSV handling of special characters that need escaping
    
    This test ensures proper CSV escaping for:
    1. Commas within data (should be quoted)
    2. Newlines within data (should be quoted) 
    3. Double quotes within data (should be escaped)
    4. Empty/None values
    """
    # Mock data with special characters that challenge CSV formatting
    special_columns = [
        {"name": "Description", "type": "text"},
        {"name": "Notes", "type": "text"},
        {"name": "Empty", "type": "text"}
    ]
    
    special_rows = [
        {"values": {
            "Description": "Task with, comma",
            "Notes": 'Text with "quotes"',
            "Empty": ""
        }},
        {"values": {
            "Description": "Text with\nnewline",
            "Notes": "Normal text",
            "Empty": None  # Test None handling
        }}
    ]
    
    with patch('common.pycoda.Pycoda.list_columns') as mock_list_columns, \
         patch('common.pycoda.Pycoda.list_rows') as mock_list_rows:
        
        mock_list_columns.return_value = json.dumps(special_columns)
        mock_list_rows.return_value = json.dumps(special_rows)
        
        runner = CliRunner()
        result = runner.invoke(clickMain, [
            'export-table', '--doc', 'test-doc', '--table', 'test-table'
        ])
        
        assert result.exit_code == 0
        
        # Verify CSV handles special characters properly
        output_lines = result.output.strip().split('\n')
        assert len(output_lines) >= 3  # Header + at least 2 data rows
        
        # Check that commas in data don't break CSV structure
        # The line with comma should be properly quoted or handled
        csv_content = result.output
        assert "Task with, comma" in csv_content
        assert "quotes" in csv_content
        
        # Verify we can parse it back as valid CSV
        import csv
        from io import StringIO
        
        csv_reader = csv.reader(StringIO(csv_content))
        rows = list(csv_reader)
        
        # Filter out empty rows (common in CSV processing)
        non_empty_rows = [row for row in rows if row]
        
        # Should have header + 2 data rows
        assert len(non_empty_rows) == 3  # Exactly header + 2 data rows
        
        # Each non-empty row should have exactly 3 fields (matching 3 columns)
        for row in non_empty_rows:
            assert len(row) == 3
            
        # Verify specific content is properly escaped and preserved
        header_row = non_empty_rows[0]
        assert header_row == ["Description", "Notes", "Empty"]
        
        data_row_1 = non_empty_rows[1] 
        assert data_row_1[0] == "Task with, comma"  # Comma preserved
        assert data_row_1[1] == 'Text with "quotes"'  # Quotes preserved
        assert data_row_1[2] == ""  # Empty string
        
        data_row_2 = non_empty_rows[2]
        assert data_row_2[0] == "Text with\nnewline"  # Newline preserved
        assert data_row_2[1] == "Normal text"
        assert data_row_2[2] == ""  # None converted to empty string

def test_export_table_with_template_name():
    """Test export-table command with template name instead of document ID
    
    This test validates the business requirement: users should be able to use
    registered template names instead of document IDs for export-table command.
    Template name "project-kickoff" should resolve to document ID "test-doc-123".
    """
    # Mock API responses with expected data structure
    mock_columns = [
        {"name": "Task", "type": "text"},
        {"name": "Owner", "type": "person"},
        {"name": "Priority", "type": "select"}
    ]
    
    mock_rows = [
        {"values": {"Task": "Setup project", "Owner": "John Doe", "Priority": "High"}},
        {"values": {"Task": "Define scope", "Owner": "Jane Smith", "Priority": "Medium"}}
    ]
    
    # Mock both the template registry and API calls
    with patch('common.template_registry.TemplateRegistry') as mock_registry_class, \
         patch('common.pycoda.Pycoda.list_columns') as mock_list_columns, \
         patch('common.pycoda.Pycoda.list_rows') as mock_list_rows:
        
        # Setup mock template registry instance
        mock_registry = mock_registry_class.return_value
        mock_registry.get_template_doc_id.return_value = "test-doc-123"
        mock_registry.is_template_registered.return_value = True
        
        # Setup API mocks 
        mock_list_columns.return_value = json.dumps(mock_columns)
        mock_list_rows.return_value = json.dumps(mock_rows)
        
        runner = CliRunner()
        result = runner.invoke(clickMain, [
            'export-table', '--doc', 'project-kickoff', '--table', 'test-table-id'
        ])
        
        # Should succeed - template name resolved to document ID
        assert result.exit_code == 0
        
        # Verify template registry was used to resolve name
        mock_registry_class.assert_called_once()
        mock_registry.get_template_doc_id.assert_called_once_with('project-kickoff')
        
        # Verify API was called with resolved document ID
        mock_list_columns.assert_called_once_with('test-doc-123', 'test-table-id')
        mock_list_rows.assert_called_once_with('test-doc-123', 'test-table-id')
        
        # Verify expected CSV output
        assert 'Task,Owner,Priority' in result.output  # Expected CSV headers
        assert 'Setup project,John Doe,High' in result.output  # Expected CSV data
        assert 'Define scope,Jane Smith,Medium' in result.output  # Expected CSV data
