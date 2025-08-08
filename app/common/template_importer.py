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