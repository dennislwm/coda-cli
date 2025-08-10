"""Template registry for managing Coda document templates"""

import json
import os
from typing import Optional, Dict

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                E X C E P T I O N S                                     |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
class TemplateNotFoundError(Exception):
    """Raised when a requested template is not found in the registry"""
    
    def __init__(self, template_name):
        """Initialize with template name for descriptive error message"""
        self.template_name = template_name
        super().__init__(f"Template '{template_name}' not found in registry")

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                    M A I N   C L A S S                                   |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
class TemplateRegistry:
    """Registry for managing template name to document ID mappings"""

    """--------+---------+---------+---------+---------+---------+---------+---------+---------|
    |                                   C O N S T R U C T O R                                  |
    |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
    def __init__(self, registry_file: str = "templates.json"):
        """Initialize template registry with file persistence
        
        Args:
            registry_file: Path to JSON file for persistence (default: templates.json)
        """
        self.registry_file = registry_file
        self._templates = self._load_templates()

    """--------+---------+---------+---------+---------+---------+---------+---------+---------|
    |                                C L A S S   M E T H O D S                                 |
    |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
    def register_template(self, name: str, doc_id: str) -> None:
        """Register a template with given name and document ID
        
        Args:
            name: Template name (must be non-empty string)
            doc_id: Document ID (must be non-empty string)
            
        Raises:
            ValueError: If name or doc_id is empty/whitespace only
        """
        if not name.strip() or not doc_id.strip():
            raise ValueError("Name and document ID cannot be empty")
        self._templates[name.strip()] = doc_id.strip()
        self._save_templates()

    def get_template_doc_id(self, name):
        """Retrieve document ID for registered template by name (legacy method)"""
        assert(name)
        if name not in self._templates:
            raise TemplateNotFoundError(name)
        return self._templates[name]

    def is_template_registered(self, name):
        """Check if template is registered by name (legacy method)"""
        assert(name)
        return name in self._templates
    
    def get_template(self, name: str) -> Optional[str]:
        """Retrieve document ID for registered template by name
        
        Args:
            name: Template name to look up
            
        Returns:
            str: Document ID if template exists, None otherwise
        """
        return self._templates.get(name.strip()) if name.strip() else None
    
    def list_templates(self) -> Dict[str, str]:
        """List all registered templates
        
        Returns:
            dict: Copy of template_name -> document_id mappings
        """
        return self._templates.copy()
    
    def remove_template(self, name: str) -> bool:
        """Remove a template from the registry
        
        Args:
            name: Template name to remove
            
        Returns:
            bool: True if template was removed, False if it didn't exist
        """
        name = name.strip()
        if name in self._templates:
            del self._templates[name]
            self._save_templates()
            return True
        return False

    """--------+---------+---------+---------+---------+---------+---------+---------+---------|
    |                                P R I V A T E   M E T H O D S                              |
    |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
    def _load_templates(self) -> Dict[str, str]:
        """Load templates from JSON file with simple error recovery"""
        try:
            if not os.path.exists(self.registry_file):
                self._save_empty_registry()
                return {}
            
            with open(self.registry_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return {k.strip(): v.strip() for k, v in data.items() 
                           if isinstance(k, str) and isinstance(v, str) 
                           and k.strip() and v.strip()}
        except (json.JSONDecodeError, IOError):
            pass
        
        self._save_empty_registry()
        return {}
    
    def _save_templates(self) -> None:
        """Save templates to JSON file using atomic write pattern"""
        temp_file = self.registry_file + '.tmp'
        try:
            with open(temp_file, 'w') as f:
                json.dump(self._templates, f, indent=2)
            # Atomic operation - replace original with temp file
            os.replace(temp_file, self.registry_file)
        except (IOError, OSError):
            # Clean up temp file on error
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
    
    def _save_empty_registry(self) -> None:
        """Create empty registry file"""
        with open(self.registry_file, 'w') as f:
            json.dump({}, f)