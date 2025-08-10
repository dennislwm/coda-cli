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

    def import_with_cli_output(self, template_file, variables_str, pycoda_client):
        """Import YAML template and create new document with CLI-specific handling"""
        import os
        
        try:
            # Check if template file exists
            if not os.path.exists(template_file):
                import click
                raise click.ClickException(f"Template file not found: {template_file}")
            
            # Read template file
            with open(template_file, "r", encoding="utf-8") as f:
                yaml_content = f.read()
            
            # Parse variables if provided
            variables = {}
            if variables_str:
                try:
                    # Parse "VAR1=value1 VAR2=value2" format with quoted values support
                    import shlex
                    # Use shlex to handle quoted arguments properly
                    try:
                        # Split respecting quotes: "DOC_NAME=My CLI Test Project" becomes one argument
                        args = shlex.split(variables_str)
                        for var_pair in args:
                            if "=" in var_pair:
                                key, value = var_pair.split("=", 1)
                                variables[key.strip()] = value.strip()
                    except Exception:
                        # Fallback to simple split if shlex fails
                        for var_assignment in variables_str.split():
                            if '=' in var_assignment:
                                key, value = var_assignment.split('=', 1)
                                variables[key.strip()] = value.strip()
                except Exception as e:
                    import click
                    raise click.ClickException(f"Invalid variables format: {str(e)}")
            
            # Create document from template
            result = self.create_document_from_template(yaml_content, variables, pycoda_client)
            
            # Display success message with document info
            doc_name = result.get("name", "Unknown")
            doc_id = result.get("id", "Unknown")
            print(f"Document created successfully!")
            print(f"Name: {doc_name}")
            print(f"ID={doc_id}")
            
            # Show variable substitutions if any were used
            if variables:
                print(f"Variables applied: {', '.join(f'{k}={v}' for k, v in variables.items())}")
                
        except Exception as e:
            # Import click here to avoid circular dependencies
            import click
            if isinstance(e, click.ClickException):
                raise
            else:
                raise click.ClickException(f"Import failed: {str(e)}")