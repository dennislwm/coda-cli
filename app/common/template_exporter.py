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
            Dict containing document metadata and sections for template generation
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

        # GREEN PHASE: Combine into structure for template generation including ownerName
        return {
            "id": doc_data["id"],
            "name": doc_data["name"],
            "ownerName": doc_data["ownerName"],  # GREEN PHASE: Add ownerName from doc_data
            "sections": sections_data
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
            document_structure: Dict with document name and sections
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

        # Convert sections from Coda API format to DocumentCreator format
        template_sections = []
        for section in document_structure["sections"]:
            template_section = {
                "name": section["name"],
                "type": section["contentType"]  # Convert contentType to type for DocumentCreator
            }
            template_sections.append(template_section)

        # Create DocumentCreator-compatible structure
        template_structure = {
            "document": {
                "name": template_name,
                "sections": template_sections
            }
        }

        # Generate YAML with proper formatting
        return yaml.dump(template_structure, default_flow_style=False, allow_unicode=True)
