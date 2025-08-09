import csv
import json
from io import StringIO


class TableDataExporter:
    """Exports Coda table data to CSV format"""
    
    def __init__(self, pycoda_client):
        """Initialize TableDataExporter with Pycoda client"""
        self.pycoda = pycoda_client
    
    def export_table_csv(self, doc_id, table_id):
        """Export table data as CSV string with error handling
        
        Args:
            doc_id: Coda document ID
            table_id: Coda table ID within the document
            
        Returns:
            str: CSV formatted string with headers and data
            
        Raises:
            Exception: If API calls fail or data cannot be processed
        """
        try:
            # Get columns to create headers
            columns_json = self.pycoda.list_columns(doc_id, table_id)
            if not columns_json or columns_json == "{}":
                return ""  # Empty CSV for no columns
                
            columns = json.loads(columns_json)
            
            # Get rows data
            rows_json = self.pycoda.list_rows(doc_id, table_id)
            if not rows_json or rows_json == "{}":
                # Return CSV with headers only if columns exist
                if columns:
                    return self._generate_csv(columns, [])
                return ""
                
            rows = json.loads(rows_json)
            
            # Generate CSV content
            return self._generate_csv(columns, rows)
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse API response: {str(e)}")
        except Exception as e:
            # Re-raise with more context
            raise Exception(f"Failed to export table data: {str(e)}")
    
    def _generate_csv(self, columns, rows):
        """Generate CSV content from columns and rows data"""
        output = StringIO()
        
        # Extract column names for headers
        if isinstance(columns, list) and columns:
            headers = [col.get('name', '') for col in columns]
        else:
            headers = []
            
        # Write CSV data
        if headers:
            writer = csv.writer(output)
            writer.writerow(headers)
            
            # Extract and write row data
            if isinstance(rows, list):
                for row in rows:
                    row_values = [
                        self._extract_cell_value(row, header) 
                        for header in headers
                    ]
                    writer.writerow(row_values)
        
        return output.getvalue()
    
    def _extract_cell_value(self, row, column_name):
        """Extract cell value from row data structure with robust None handling"""
        # Handle typical Coda API response structure
        if isinstance(row, dict) and 'values' in row:
            values = row['values']
            if isinstance(values, dict):
                cell_value = values.get(column_name, "")
                # Ensure string conversion and handle None values
                return str(cell_value) if cell_value is not None else ""
        return ""