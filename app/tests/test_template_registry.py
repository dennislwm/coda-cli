"""Test cases for TemplateRegistry functionality"""

import pytest
from common.template_registry import TemplateRegistry, TemplateNotFoundError


class TestTemplateRegistry:
    """Test cases for TemplateRegistry class"""

    def test_register_and_retrieve_template(self):
        """Test basic template registration and retrieval
        
        This test validates the core business requirement: register a template
        with a name and document ID, then retrieve it by name.
        """
        # Arrange: Create registry and test data
        registry = TemplateRegistry()
        template_name = "project-tracker"
        document_id = "doc123"
        
        # Act: Register template
        registry.register_template(template_name, document_id)
        
        # Assert: Retrieve template returns correct document ID
        retrieved_doc_id = registry.get_template_doc_id(template_name)
        assert retrieved_doc_id == document_id
        
        # Assert: Template is now registered
        assert registry.is_template_registered(template_name) == True

    def test_get_nonexistent_template_raises_error(self):
        """Test that retrieving non-existent template raises TemplateNotFoundError
        
        This test validates error handling business requirement: when a user
        requests a template that doesn't exist, they should get a clear error
        message that includes the template name they requested.
        """
        # Arrange: Create empty registry
        registry = TemplateRegistry()
        nonexistent_template = "nonexistent-template"
        
        # Act & Assert: Expect TemplateNotFoundError with template name in message
        with pytest.raises(TemplateNotFoundError) as exc_info:
            registry.get_template_doc_id(nonexistent_template)
        
        # Assert: Error message includes template name for user clarity
        assert nonexistent_template in str(exc_info.value)
