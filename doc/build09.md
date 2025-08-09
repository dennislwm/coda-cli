# Build 09: TDD Design - Table Data Backup System

**Target:** TableDataExporter module (~100-150 lines)  
**Timeline:** 2 workdays  
**Dependencies:** Pycoda list_columns() and list_rows() API calls

## TDD Implementation Plan

### Core Business Requirements

- CSV export: `export-table --doc DOC_ID --table TABLE_ID [--output FILE]`
- Performance: <5 seconds for typical tables
- Error handling: Invalid IDs, file permissions, API failures
- UTF-8 encoding support

### Test Structure

```text
app/tests/test_table_data_exporter.py  # Single test file
```

## TDD Cycles

### Cycle 1: Core Export Functionality

**Red Phase Test:**
```python
def test_export_table_basic():
    runner = CliRunner()
    result = runner.invoke(clickMain, [
        'export-table', '--doc', 'test-doc', '--table', 'test-table'
    ])
    
    assert result.exit_code == 0
    assert 'Name,Status,Date' in result.output
    assert 'Task 1,Active,2024-01-01' in result.output
```

**Green Phase Implementation:**

Add CLI command to `coda.py`:

```python
@clickMain.command()
@click.option('--doc', required=True)
@click.option('--table', required=True)
@click.option('--output', '-o')
@click.pass_obj
def export_table(objCoda, doc, table, output):
    objCoda.export_table(doc, table, output)
```

Add method to Coda class:

```python
def export_table(self, doc_id, table_id, output_file=None):
    from common.table_data_exporter import TableDataExporter
    
    exporter = TableDataExporter(self.objCoda)
    csv_content = exporter.export_table_csv(doc_id, table_id)
    
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(csv_content)
        print(f"Exported to {output_file}")
    else:
        print(csv_content)
```

Create `app/common/table_data_exporter.py`:

```python
import csv
import json
from io import StringIO

class TableDataExporter:
    def __init__(self, pycoda_client):
        self.pycoda = pycoda_client
    
    def export_table_csv(self, doc_id, table_id):
        columns_json = self.pycoda.list_columns(doc_id, table_id)
        rows_json = self.pycoda.list_rows(doc_id, table_id)
        
        columns = json.loads(columns_json)
        rows = json.loads(rows_json)
        
        return self._generate_csv(columns, rows)
    
    def _generate_csv(self, columns, rows):
        output = StringIO()
        
        if isinstance(columns, list) and columns:
            headers = [col.get('name', '') for col in columns]
            writer = csv.writer(output)
            writer.writerow(headers)
            
            if isinstance(rows, list):
                for row in rows:
                    row_values = []
                    for header in headers:
                        cell_value = self._extract_cell_value(row, header)
                        row_values.append(str(cell_value) if cell_value else "")
                    writer.writerow(row_values)
        
        return output.getvalue()
    
    def _extract_cell_value(self, row, column_name):
        if isinstance(row, dict) and 'values' in row:
            values = row['values']
            if isinstance(values, dict):
                return values.get(column_name, "")
        return ""
```

### Cycle 2: Error Handling

**Red Phase Test:**

```python
def test_export_table_errors():
    runner = CliRunner()
    
    # Test invalid document ID
    result = runner.invoke(clickMain, [
        'export-table', '--doc', 'invalid', '--table', 'test-table'
    ])
    assert result.exit_code != 0
    assert "error" in result.output.lower()
    
    # Test file permission error
    result = runner.invoke(clickMain, [
        'export-table', '--doc', 'test', '--table', 'test', 
        '--output', '/root/readonly.csv'
    ])
    assert result.exit_code != 0
```

**Green Phase Implementation:**

Update Coda method with error handling:

```python
def export_table(self, doc_id, table_id, output_file=None):
    try:
        from common.table_data_exporter import TableDataExporter
        exporter = TableDataExporter(self.objCoda)
        csv_content = exporter.export_table_csv(doc_id, table_id)
        
        if not csv_content.strip():
            print("Warning: No data found")
            return
            
        if output_file:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(csv_content)
                print(f"Exported to {output_file}")
            except PermissionError:
                raise click.ClickException(f"Permission denied: {output_file}")
            except Exception as e:
                raise click.ClickException(f"File error: {str(e)}")
        else:
            print(csv_content)
    except Exception as e:
        raise click.ClickException(f"Export failed: {str(e)}")
```

Update TableDataExporter with error handling:

```python
def export_table_csv(self, doc_id, table_id):
    try:
        columns_json = self.pycoda.list_columns(doc_id, table_id)
        if not columns_json or columns_json == "{}":
            return ""
            
        rows_json = self.pycoda.list_rows(doc_id, table_id)
        if not rows_json or rows_json == "{}":
            columns_data = json.loads(columns_json)
            return self._generate_csv(columns_data, [])
            
        columns = json.loads(columns_json)
        rows = json.loads(rows_json)
        return self._generate_csv(columns, rows)
        
    except json.JSONDecodeError:
        return ""
    except Exception as e:
        raise Exception(f"Export failed: {str(e)}")
```

### Cycle 3: File Output and Unicode

**Red Phase Test:**

```python
def test_export_to_file_and_unicode():
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        temp_file = tmp.name
    
    try:
        # Mock Unicode data
        unicode_columns = [{"name": "项目"}, {"name": "状态"}]
        unicode_rows = [{"values": {"项目": "测试", "状态": "完成"}}]
        
        with patch('common.pycoda.Pycoda.list_columns') as mock_cols, \
             patch('common.pycoda.Pycoda.list_rows') as mock_rows:
            
            mock_cols.return_value = json.dumps(unicode_columns)
            mock_rows.return_value = json.dumps(unicode_rows)
            
            runner = CliRunner()
            result = runner.invoke(clickMain, [
                'export-table', '--doc', 'test', '--table', 'test',
                '--output', temp_file
            ])
            
            assert result.exit_code == 0
            assert os.path.exists(temp_file)
            
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "项目,状态" in content
                assert "测试,完成" in content
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
```

**Green Phase:** Unicode support is already handled by UTF-8 encoding in the existing implementation.

### Cycle 4: Performance and Integration

**Red Phase Test:**

```python
def test_export_performance_and_large_data():
    # Create large dataset
    large_columns = [{"name": f"Col{i}"} for i in range(10)]
    large_rows = [
        {"values": {f"Col{j}": f"Data{i}_{j}" for j in range(10)}}
        for i in range(1000)
    ]
    
    with patch('common.pycoda.Pycoda.list_columns') as mock_cols, \
         patch('common.pycoda.Pycoda.list_rows') as mock_rows:
        
        mock_cols.return_value = json.dumps(large_columns)
        mock_rows.return_value = json.dumps(large_rows)
        
        start_time = time.time()
        
        runner = CliRunner()
        result = runner.invoke(clickMain, [
            'export-table', '--doc', 'test', '--table', 'test'
        ])
        
        execution_time = time.time() - start_time
        
        assert result.exit_code == 0
        assert execution_time < 5.0  # Performance requirement
        assert result.output.count('\n') >= 1000  # All rows present
```

**Green Phase:** Existing implementation should handle this. Optimize if needed:

```python
def _generate_csv(self, columns, rows):
    output = StringIO()
    
    if isinstance(columns, list) and columns:
        headers = [col.get('name', '') for col in columns]
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        
        if isinstance(rows, list):
            for row in rows:
                row_values = [
                    str(self._extract_cell_value(row, header) or "")
                    for header in headers
                ]
                writer.writerow(row_values)
    
    return output.getvalue()
```

## Integration Test

**Complete End-to-End Test:**

```python
def test_end_to_end_workflow():
    realistic_columns = [
        {"name": "Task", "type": "text"},
        {"name": "Assignee", "type": "person"},
        {"name": "Status", "type": "select"}
    ]
    
    realistic_rows = [
        {"values": {"Task": "Setup", "Assignee": "John", "Status": "Done"}},
        {"values": {"Task": "Review", "Assignee": "Jane", "Status": "Pending"}}
    ]
    
    with patch('common.pycoda.Pycoda.list_columns') as mock_cols, \
         patch('common.pycoda.Pycoda.list_rows') as mock_rows:
        
        mock_cols.return_value = json.dumps(realistic_columns)
        mock_rows.return_value = json.dumps(realistic_rows)
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            temp_file = tmp.name
        
        try:
            runner = CliRunner()
            result = runner.invoke(clickMain, [
                'export-table', '--doc', 'real-doc', '--table', 'real-table',
                '--output', temp_file
            ])
            
            assert result.exit_code == 0
            assert "exported to" in result.output.lower()
            
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "Task,Assignee,Status" in content
                assert "Setup,John,Done" in content
                assert "Review,Jane,Pending" in content
                
                lines = content.strip().split('\n')
                assert len(lines) == 3  # Header + 2 data rows
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
```

## Implementation Timeline

### Day 1

**Morning (4 hours):**

- TDD Cycle 1: Core export functionality
- CLI command and basic CSV generation

**Afternoon (4 hours):**

- TDD Cycle 2: Error handling
- File output and robust error messages

### Day 2

**Morning (4 hours):**

- TDD Cycle 3: Unicode support and file operations
- TDD Cycle 4: Performance optimization

**Afternoon (4 hours):**

- Integration testing and edge cases
- Code review and documentation

## Success Criteria

### Functional Requirements

- [ ] `export-table --doc DOC --table TABLE` outputs CSV to stdout
- [ ] `export-table --doc DOC --table TABLE --output file.csv` creates file
- [ ] Proper CSV headers from column names
- [ ] UTF-8 encoding handles international characters
- [ ] Export completes within 5 seconds for typical tables
- [ ] Meaningful error messages for invalid inputs

### Quality Gates

- [ ] 85%+ test coverage
- [ ] All TDD cycles pass
- [ ] Performance benchmarks met
- [ ] Error handling validated
- [ ] Integration with existing Pycoda patterns maintained

### Out of Scope

- Data import/restoration
- Multiple table export
- Automated scheduling
- Formula preservation
- Metadata export

## Economic Impact

**Development Cost:** 2 days (16 hours)
**User Value:** Eliminates 15-30 minutes manual export per table
**ROI:** Break-even after 2-3 export operations

This streamlined TDD approach delivers the essential CSV export functionality with minimal complexity while maintaining robust testing and error handling.
