"""
TemplateImporter: Efficient YAML template parsing and variable substitution
"""
import yaml
import re


class TemplateImporter:
    """Converts YAML templates back to document structures with variable substitution"""
    
    def __init__(self):
        self._var_pattern = re.compile(r'\{\{(\w+)\}\}')  # Compiled regex for efficiency

    def parse_yaml_template(self, yaml_content):
        """Parse YAML template to document structure"""
        try:
            data = yaml.safe_load(yaml_content)
            if not data or "document" not in data:
                raise ValueError("Invalid template: missing 'document' key")
            return data
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}")
    
    def substitute_variables(self, yaml_content, variables):
        """Efficient variable substitution using regex"""
        def replacer(match):
            var_name = match.group(1)
            return str(variables.get(var_name, match.group(0)))
        
        return self._var_pattern.sub(replacer, yaml_content)
    
    def create_document_from_template(self, yaml_content, variables, pycoda_client):
        """Create a new Coda document from YAML template with variable substitution
        
        Args:
            yaml_content: String containing YAML template
            variables: Dict mapping variable names to replacement values
            pycoda_client: Pycoda instance for API calls
            
        Returns:
            Dict containing document creation result with id and name
            
        Raises:
            ValueError: If template is invalid or document creation fails
        """
        try:
            # Step 1: Substitute variables in template
            substituted_yaml = self.substitute_variables(yaml_content, variables)
            
            # Step 2: Parse the substituted YAML template
            template_structure = self.parse_yaml_template(substituted_yaml)
            
            # Step 3: Extract document name from parsed structure
            document_name = template_structure["document"]["name"]
            
            # Step 4: Create the document using Pycoda client
            result = pycoda_client.create_document(document_name)
            
            # Step 5: Check for errors in document creation
            if "error" in result:
                raise ValueError(f"Document creation failed: {result['error']}")
                
            return result
            
        except Exception as e:
            raise ValueError(f"Failed to create document from template: {str(e)}") from e