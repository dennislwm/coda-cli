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

        # Get sections/pages data
        sections_json = self.pycoda.list_sections(doc_id)
        sections_data = json.loads(sections_json)

        # Combine into structure for template generation
        return {
            "id": doc_data["id"],
            "name": doc_data["name"],
            "sections": sections_data
        }

    def detect_variables(self, document_structure):
        """Detect template variables conservatively from document structure

        Args:
            document_structure: Dict with document name and sections

        Returns:
            Dict mapping variable names to detected values (max 7 variables)
        """
        import re

        variables = {}

        # Pattern 1: PROJECT_NAME from document names
        doc_name = document_structure["name"]

        # Remove .coda extension first
        clean_name = doc_name.replace(".coda", "")

        # Conservative patterns based on real data:
        # "TrackMySubs", "TrackMyScreen", "PokemonLeesarebest", etc.
        if clean_name and " " not in clean_name:  # Single word/compound word only
            variables["PROJECT_NAME"] = clean_name
        elif clean_name == "Question Voting and Polling":  # Handle specific known multi-word
            # Conservative: only handle clear, specific cases
            pass  # Don't detect variables from complex multi-word names

        # Conservative approach: Start with just PROJECT_NAME pattern
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