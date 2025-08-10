import csv
from io import StringIO
from .base_exporter import BaseExporter


class TableDataExporter(BaseExporter):
    """Exports Coda table data to CSV format"""
    
    def __init__(self, pycoda_client):
        """Initialize TableDataExporter with Pycoda client"""
        super().__init__(pycoda_client)
    
    def export_table_csv(self, doc_id, table_id):
        """Export table data as CSV string"""
        try:
            # Get columns to create headers
            columns_json = self.pycoda.list_columns(doc_id, table_id)
            if not columns_json or columns_json == "{}":
                return ""  # Empty CSV for no columns
                
            columns = self._parse_api_response(columns_json)
            
            # Get rows data
            rows_json = self.pycoda.list_rows(doc_id, table_id)
            if not rows_json or rows_json == "{}":
                # Return CSV with headers only if columns exist
                if columns:
                    return self._generate_csv(columns, [])
                return ""
                
            rows = self._parse_api_response(rows_json)
            
            # Generate CSV content
            return self._generate_csv(columns, rows)
            
        except Exception as e:
            if "JSON" in str(e):
                raise Exception(f"Failed to parse API response: {str(e)}")
            raise
        except Exception as e:
            # Re-raise with more context
            raise Exception(f"Failed to export table data: {str(e)}")
    
    def _generate_csv(self, columns, rows):
        """Generate CSV content from columns and rows data"""
        output = StringIO()
        
        # Extract column names for headers and create name-to-id mapping
        if isinstance(columns, list) and columns:
            headers = [col.get('name', '') for col in columns]
            column_map = {col.get('name', ''): col.get('id', '') for col in columns}
        else:
            headers = []
            column_map = {}
            
        # Write CSV data
        if headers:
            writer = csv.writer(output)
            writer.writerow(headers)
            
            # Extract and write row data
            if isinstance(rows, list):
                for row in rows:
                    row_values = [
                        self._extract_cell_value(row, header, column_map) 
                        for header in headers
                    ]
                    writer.writerow(row_values)
        
        return output.getvalue()
    

    def _extract_cell_value(self, row, column_name, column_map):
        """Extract cell value from row data structure using column ID mapping"""
        # Handle typical Coda API response structure
        if isinstance(row, dict) and 'values' in row:
            values = row['values']
            if isinstance(values, dict):
                # Use column ID (not name) to lookup the actual value
                column_id = column_map.get(column_name, "")
                if column_id:
                    cell_value = values.get(column_id, "")
                    # Ensure string conversion and handle None values
                    return str(cell_value) if cell_value is not None else ""
        return ""