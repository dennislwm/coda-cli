"""
DocumentCreator module for Interactive Document Builder
Minimal implementation following TDD approach
"""


class DocumentCreator:
    """Creates Coda documents from YAML templates"""

    def __init__(self, pycoda_client):
        """Initialize DocumentCreator with Pycoda client

        Args:
            pycoda_client: Instance of Pycoda for API operations
        """
        self.pycoda = pycoda_client

    def load_template(self, template_path):
        """Load and parse YAML template from file
        
        Args:
            template_path: Path to YAML template file
            
        Returns:
            Dict containing parsed template structure
        """
        import yaml
        
        with open(template_path, 'r') as file:
            return yaml.safe_load(file)

    def substitute_variables(self, content, variables):
        """Replace {{VARIABLE}} patterns with values in strings and nested structures

        Args:
            content: String or dict containing {{VARIABLE}} patterns
            variables: Dict mapping variable names to replacement values

        Returns:
            Content with variables substituted
        """
        if isinstance(content, str):
            # Handle string substitution
            result = content
            for key, value in variables.items():
                pattern = f"{{{{{key}}}}}"  # {{KEY}}
                result = result.replace(pattern, str(value))
            return result
        elif isinstance(content, dict):
            # Handle dictionary substitution recursively
            return {key: self.substitute_variables(value, variables)
                    for key, value in content.items()}
        elif isinstance(content, list):
            # Handle list substitution recursively
            return [self.substitute_variables(item, variables) for item in content]
        else:
            # Return non-template content unchanged
            return content

    def create_document_from_template(self, template):
        """Create a Coda document from a processed template
        
        Args:
            template: Dict containing document structure with name and sections
            
        Returns:
            Dict containing document_id and creation details
        """
        document_info = template["document"]
        
        # Create the document
        doc_result = self.pycoda.create_document(document_info["name"])
        document_id = doc_result["id"]
        
        # Add sections to the document
        for section in document_info.get("sections", []):
            self.pycoda.add_section(
                document_id,
                section["name"],
                section["type"],
                section.get("content", "")
            )
        
        return {"document_id": document_id}