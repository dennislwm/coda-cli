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
        self.client = pycoda_client

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
        else:
            # Return non-template content unchanged
            return content