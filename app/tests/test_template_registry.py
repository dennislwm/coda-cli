"""Test cases for TemplateRegistry functionality"""

import tempfile
import os
import pytest
from common.template_registry import TemplateRegistry, TemplateNotFoundError


class TestTemplateRegistry:
    """Test cases for TemplateRegistry class"""

    def test_core_operations_with_persistence(self):
        """Test CRUD operations and persistence across CLI sessions
        
        Validates core business requirement: templates persist between CLI sessions
        """
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            registry_file = tmp.name
        
        try:
            # Basic CRUD operations
            registry = TemplateRegistry(registry_file)
            registry.register_template("project-tracker", "doc123")
            assert registry.get_template("project-tracker") == "doc123"
            assert len(registry.list_templates()) == 1
            assert registry.list_templates()["project-tracker"] == "doc123"
            
            # Critical: Persistence across CLI sessions
            registry2 = TemplateRegistry(registry_file)
            assert registry2.get_template("project-tracker") == "doc123"
            
            # Template removal persists
            assert registry2.remove_template("project-tracker") == True
            assert registry2.get_template("project-tracker") is None
            
            # Verify removal persisted across sessions
            registry3 = TemplateRegistry(registry_file)
            assert registry3.get_template("project-tracker") is None
            assert len(registry3.list_templates()) == 0
            
        finally:
            if os.path.exists(registry_file):
                os.unlink(registry_file)

    def test_error_handling_and_recovery(self):
        """Test input validation, corrupted file recovery, and error handling
        
        Validates production reliability: system handles errors gracefully
        """
        # Test corrupted JSON auto-recovery
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp.write('{"incomplete": "json')  # Corrupted JSON
            registry_file = tmp.name
        
        try:
            # System should auto-recover from corrupted files
            registry = TemplateRegistry(registry_file)
            assert registry.list_templates() == {}
            
            # Input validation prevents bad data
            with pytest.raises(ValueError) as exc_info:
                registry.register_template("", "doc123")
            assert "cannot be empty" in str(exc_info.value)
            
            with pytest.raises(ValueError):
                registry.register_template("test", "")
            
            # Non-existent template lookups are graceful
            assert registry.get_template("nonexistent") is None
            assert registry.remove_template("nonexistent") == False
            
            # Legacy method provides specific error for compatibility
            with pytest.raises(TemplateNotFoundError) as exc_info:
                registry.get_template_doc_id("nonexistent")
            assert "nonexistent" in str(exc_info.value)
            
            # System continues working after errors
            registry.register_template("recovery-test", "doc456")
            assert registry.get_template("recovery-test") == "doc456"
            
        finally:
            if os.path.exists(registry_file):
                os.unlink(registry_file)

    def test_legacy_method_compatibility(self):
        """Test backward compatibility with existing methods"""
        registry = TemplateRegistry()
        registry.register_template("test", "doc123")
        
        # Legacy methods should continue working
        assert registry.get_template_doc_id("test") == "doc123"
        assert registry.is_template_registered("test") == True
        assert registry.is_template_registered("nonexistent") == False