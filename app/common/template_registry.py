"""Template registry for managing Coda document templates"""

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
    def __init__(self):
        """Initialize template registry with empty storage"""
        self._templates = {}

    """--------+---------+---------+---------+---------+---------+---------+---------+---------|
    |                                C L A S S   M E T H O D S                                 |
    |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
    def register_template(self, name, doc_id):
        """Register a template with given name and document ID"""
        assert(name)
        assert(doc_id)
        self._templates[name] = doc_id

    def get_template_doc_id(self, name):
        """Retrieve document ID for registered template by name"""
        assert(name)
        if name not in self._templates:
            raise TemplateNotFoundError(name)
        return self._templates[name]

    def is_template_registered(self, name):
        """Check if template is registered by name"""
        assert(name)
        return name in self._templates
