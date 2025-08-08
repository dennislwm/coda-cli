"""
TemplateExporter module for Automated YAML Template Export
Minimal implementation following TDD approach
"""


class TemplateExporter:
    """Exports Coda documents to reusable YAML templates"""

    def __init__(self, pycoda_client):
        """Initialize TemplateExporter with Pycoda client

        Args:
            pycoda_client: Instance of Pycoda for API operations
        """
        self.pycoda = pycoda_client


    def extract_document_structure(self, doc_id):
        """Extract document structure from Coda API responses

        Args:
            doc_id: Coda document ID

        Returns:
            Dict containing document metadata, sections, and tables for template generation
        """
        import json

        # Get document metadata
        doc_json = self.pycoda.get_doc(doc_id)
        doc_data = json.loads(doc_json)

        # Get sections/pages data - handle both JSON array and concatenated JSON format from Pycoda
        sections_json = self.pycoda.list_sections(doc_id)
        
        # Parse sections data - handle both formats
        sections_data = []
        if sections_json and sections_json != "{}":
            try:
                # Try parsing as JSON array first (from tests)
                parsed_sections = json.loads(sections_json)
                if isinstance(parsed_sections, list):
                    sections_data = parsed_sections
                else:
                    sections_data = [parsed_sections]
            except json.JSONDecodeError:
                # Fall back to concatenated JSON objects parsing (from real API)
                decoder = json.JSONDecoder()
                idx = 0
                while idx < len(sections_json.strip()):
                    try:
                        obj, end_idx = decoder.raw_decode(sections_json, idx)
                        sections_data.append(obj)
                        idx = end_idx
                    except json.JSONDecodeError:
                        # Skip any whitespace or invalid characters
                        idx += 1
                        if idx >= len(sections_json):
                            break
                        continue

        # GREEN PHASE: Get tables data - handle both JSON array and concatenated JSON format from Pycoda
        tables_json = self.pycoda.list_tables(doc_id)
        
        # Parse tables data - handle both formats (similar to sections)
        tables_data = []
        if tables_json and tables_json != "{}":
            try:
                # Try parsing as JSON array first (from tests)
                parsed_tables = json.loads(tables_json)
                if isinstance(parsed_tables, list):
                    tables_data = parsed_tables
                else:
                    tables_data = [parsed_tables]
            except json.JSONDecodeError:
                # Fall back to concatenated JSON objects parsing (from real API)
                decoder = json.JSONDecoder()
                idx = 0
                while idx < len(tables_json.strip()):
                    try:
                        obj, end_idx = decoder.raw_decode(tables_json, idx)
                        tables_data.append(obj)
                        idx = end_idx
                    except json.JSONDecodeError:
                        # Skip any whitespace or invalid characters
                        idx += 1
                        if idx >= len(tables_json):
                            break
                        continue

        # NESTED KEYS PHASE: Get column data for each table
        for table in tables_data:
            table_id = table["id"]
            columns_json = self.pycoda.list_columns(doc_id, table_id)
            
            # Parse columns data - handle both formats (similar to tables/sections)
            columns_data = []
            if columns_json and columns_json != "{}":
                try:
                    # Try parsing as JSON array first (from tests)
                    parsed_columns = json.loads(columns_json)
                    if isinstance(parsed_columns, list):
                        columns_data = parsed_columns
                    else:
                        columns_data = [parsed_columns]
                except json.JSONDecodeError:
                    # Fall back to concatenated JSON objects parsing (from real API)
                    decoder = json.JSONDecoder()
                    idx = 0
                    while idx < len(columns_json.strip()):
                        try:
                            obj, end_idx = decoder.raw_decode(columns_json, idx)
                            columns_data.append(obj)
                            idx = end_idx
                        except json.JSONDecodeError:
                            # Skip any whitespace or invalid characters
                            idx += 1
                            if idx >= len(columns_json):
                                break
                            continue
            
            # Add columns to table data
            table["columns"] = columns_data

        # NESTED KEYS PHASE: Combine into structure for template generation including ownerName, tables, and columns
        return {
            "id": doc_data["id"],
            "name": doc_data["name"],
            "ownerName": doc_data["ownerName"],  # GREEN PHASE: Add ownerName from doc_data
            "sections": sections_data,
            "tables": tables_data  # GREEN PHASE: Add tables data with columns
        }

    def detect_variables(self, document_structure):
        """Detect template variables conservatively from document structure

        Args:
            document_structure: Dict with document name, ownerName, and sections

        Returns:
            Dict mapping variable names to detected values (max 7 variables)
        """
        import re

        variables = {}

        # GREEN PHASE: Pattern 1: DOC_NAME from document names (renamed from PROJECT_NAME)
        doc_name = document_structure["name"]

        # Remove .coda extension first
        clean_name = doc_name.replace(".coda", "")

        # Conservative patterns based on real data:
        # "TrackMySubs", "TrackMyScreen", "PokemonLeesarebest", etc.
        if clean_name and " " not in clean_name:  # Single word/compound word only
            variables["DOC_NAME"] = clean_name  # GREEN PHASE: Changed from PROJECT_NAME
        elif clean_name == "Question Voting and Polling":  # Handle specific known multi-word
            # Conservative: only handle clear, specific cases
            pass  # Don't detect variables from complex multi-word names

        # GREEN PHASE: Pattern 2: OWNER_NAME from document ownerName field
        if "ownerName" in document_structure and document_structure["ownerName"]:
            owner_name = document_structure["ownerName"]
            if owner_name.strip():  # Only if non-empty after stripping
                variables["OWNER_NAME"] = owner_name

        # Conservative approach: Start with DOC_NAME and OWNER_NAME patterns
        # Additional patterns (TEAM_NAME, STATUS, etc.) can be added in next iterations

        return variables

    def generate_yaml_template(self, document_structure, detected_variables):
        """Generate YAML template with variable substitution for DocumentCreator

        Args:
            document_structure: Dict with document name, sections, and tables
            detected_variables: Dict mapping variable names to values

        Returns:
            String containing YAML template with {{VARIABLE}} placeholders
        """
        import yaml

        # Apply variable substitution to document name
        doc_name = document_structure["name"]
        template_name = doc_name

        # Replace detected variables with template placeholders
        for var_name, var_value in detected_variables.items():
            template_name = template_name.replace(var_value, f"{{{{{var_name}}}}}")

        # NESTED KEYS PHASE: Group tables by parent section name with column definitions
        tables_by_section = {}
        if "tables" in document_structure and document_structure["tables"]:
            for table in document_structure["tables"]:
                parent_section_name = table["parent"]["name"]
                if parent_section_name not in tables_by_section:
                    tables_by_section[parent_section_name] = []
                
                # NESTED KEYS PHASE: Create table entry with column definitions
                table_entry = {"name": table["name"]}
                
                # Add columns if they exist
                if "columns" in table and table["columns"]:
                    table_columns = []
                    for column in table["columns"]:
                        column_entry = {
                            "name": column["name"],
                            "type": column.get("type", "column")
                        }
                        
                        # Add format information if available
                        if "format" in column:
                            column_entry["format"] = column["format"]
                        
                        # Add display setting
                        if "display" in column:
                            column_entry["display"] = column["display"]
                        
                        # Add calculated field and formula if it's a calculated column
                        if column.get("calculated", False):
                            column_entry["calculated"] = True
                            if "formula" in column:
                                column_entry["formula"] = column["formula"]
                        
                        table_columns.append(column_entry)
                    
                    table_entry["columns"] = table_columns
                
                tables_by_section[parent_section_name].append(table_entry)

        # Convert sections from Coda API format to nested DocumentCreator format
        template_sections = []
        for section in document_structure["sections"]:
            template_section = {
                "name": section["name"],
                "type": section["contentType"]  # Convert contentType to type for DocumentCreator
            }
            
            # GREEN PHASE: Add tables to section if this section has tables
            section_name = section["name"]
            if section_name in tables_by_section:
                template_section["tables"] = tables_by_section[section_name]
            
            template_sections.append(template_section)

        # Create DocumentCreator-compatible structure with nested tables
        template_structure = {
            "document": {
                "name": template_name,
                "sections": template_sections
            }
        }

        # GREEN PHASE: No longer add tables at document level - they're nested under sections

        # Generate YAML with proper formatting
        return yaml.dump(template_structure, default_flow_style=False, allow_unicode=True)

